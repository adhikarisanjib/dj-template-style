from django.shortcuts import render, redirect
from django.db.models import OuterRef, Subquery

from .models import Person, Address, Contact
from .forms import PersonForm, AddressForm, ContactForm


def person_list_view(request):
    search_text = request.GET.get('search', None)
    filter_field = request.GET.get('filter-field', None)

    if search_text:
        if filter_field:
            filter_field = f'{filter_field}__icontains'
            persons = Person.objects.prefetch_related('address_set', 'contact_set').filter(**{filter_field: search_text})
        else:
            persons = Person.objects.prefetch_related('address_set', 'contact_set').filter(name__icontains=search_text)

    else:
        persons = Person.objects.prefetch_related('address_set', 'contact_set').all()

    return render(request, 'person_list.html', {'persons': persons})


def person_create_view(request):
    # Check if the user wants to start a new form (e.g., clicked "Add" in the list view)
    if request.GET.get("new") == "1":
        request.session.pop('person_create_data', None)
        request.session.pop('current_step', None)

    # Check if the user wants to cancel the form
    if request.GET.get("cancel") == "1":
        request.session.pop('person_create_data', None)
        request.session.pop('current_step', None)
        return redirect('person_list')

    # Initialize session data if not set
    if 'person_create_data' not in request.session:
        request.session['person_create_data'] = {}
        request.session['current_step'] = 1

    current_step = request.session['current_step']

    # Mapping step numbers to their respective forms
    step_forms = {
        1: PersonForm,
        2: AddressForm,
        3: ContactForm,
    }

    FormClass = step_forms[current_step]

    if request.method == 'POST':
        if 'prev' in request.POST:  # Handle "Previous" button
            if current_step > 1:
                request.session['current_step'] -= 1
                request.session.modified = True
            return redirect('person_create')

        form = FormClass(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data.copy()
            
            # Format birth date if applicable as session data cannot store datetime objects
            if 'birth_date' in form_data:  
                form_data['birth_date'] = form_data['birth_date'].strftime('%Y-%m-%d')

            # Store form data for the current step
            request.session['person_create_data'][f'step_{current_step}'] = form_data
            request.session.modified = True  # Ensure session is updated

            # Move to the next step
            if current_step < 3:
                request.session['current_step'] += 1
                return redirect('person_create')
            else:
                # Final step: Save data and clear session
                data = request.session.pop('person_create_data')
                request.session.pop('current_step', None)

                person = Person.objects.create(**data['step_1'])
                Address.objects.create(person=person, **data['step_2'])
                Contact.objects.create(person=person, **data['step_3'])

                # Redirect after completion
                return redirect('person_list')  

    else:
        # Prefill form with session data if available
        initial_data = request.session['person_create_data'].get(f'step_{current_step}', {})
        form = FormClass(initial=initial_data)

    return render(request, 'person_create.html', {'form': form, 'current_step': current_step})


def profile_view(request, person_id):
    person = Person.objects.prefetch_related('address_set', 'contact_set').get(id=person_id)
    return render(request, 'profile.html', {'person': person})
