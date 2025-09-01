from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.db import transaction  # <-- Import transaction
from django.contrib import messages  # <-- Import messages for feedback

# Models and Forms
from travella.domains.forms.signup_forms import Step1Form, Step2Form, Step3Form
from travella.domains.models.account_models import Account, AccountDetail
from travella.services import access_log_service
from travella.services.access_log_service import AccessLogForm

FORMS = [
    ("step1", Step1Form),
    ("step2", Step2Form),
    ("step3", Step3Form),
]

TEMPLATE = "auth/sign-up.html"


class SignUpView(View):

    def get(self, request):
        step = int(request.GET.get('step', 1))
        if step == 1:
            request.session['signup_data'] = {}
        try:
            form_class = FORMS[step - 1][1]
            initial_data = request.session.get('signup_data', {}).get(f'step_{step}', {})
            form = form_class(initial=initial_data)
        except IndexError:
            return redirect(reverse('sign_up'))

        context = {
            'form': form, 'step': step, 'total_steps': len(FORMS),
            'progress_percentage': int(((step - 1) / len(FORMS)) * 100)
        }
        return render(request, TEMPLATE, context)


    def post(self, request):
        step = int(request.POST.get('step', 1))

        if 'prev_step' in request.POST:
            prev_step = step - 1
            return redirect(f"{reverse('sign_up')}?step={prev_step}")

        if 'skip_step' in request.POST:
            signup_data = request.session.get('signup_data', {})
            signup_data[f'step_{step}'] = {}
            request.session['signup_data'] = signup_data
            if step == len(FORMS):
                return self.complete_signup(request)
            else:
                next_step = step + 1
                return redirect(f"{reverse('sign_up')}?step={next_step}")

        try:
            form_class = FORMS[step - 1][1]
            form = form_class(request.POST, request.FILES)
        except IndexError:
            return redirect(reverse('sign_up'))

        if form.is_valid():
            signup_data = request.session.get('signup_data', {})

            signup_data[f'step_{step}'] = form.cleaned_data
            request.session['signup_data'] = signup_data

            if step == len(FORMS):
                return self.complete_signup(request)
            else:
                next_step = step + 1
                return redirect(f"{reverse('sign_up')}?step={next_step}")

        context = {
            'form': form, 'step': step, 'total_steps': len(FORMS),
            'progress_percentage': int(((step - 1) / len(FORMS)) * 100)
        }
        return render(request, TEMPLATE, context)

    def complete_signup(self, request):
        final_data = {}
        signup_data = request.session.get('signup_data', {})
        for i in range(len(FORMS)):
            step_data = signup_data.get(f'step_{i + 1}', {})
            final_data.update(step_data)


        email = final_data.get('email')
        password = final_data.get('password')


        if not email or not password:
            messages.error(request, "Something went wrong, please start over.")
            return redirect('sign_up')


        if Account.objects.filter(email=email).exists():
            messages.error(request, "This email address is already in use.")

            del request.session['signup_data']
            return redirect('sign_up')
        try:
            with transaction.atomic():

                new_account = Account.objects.create_user(
                    email=email,
                    password=password,
                )


                AccountDetail.objects.create(
                    account=new_account,
                    name=final_data.get('full_name'),
                    phone=final_data.get('phone_number'),
                    address=final_data.get('address'),
                    photo=final_data.get('profile_photo')
                )

                access_log_service.save_log(AccessLogForm.sing_up_success_form(), new_account.id)

                print(f"Successfully created account for {email}")

        except Exception as e:

            print(f"ERROR during signup: {e}")
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect('sign_up')

        del request.session['signup_data']
        messages.success(request, "Your account has been created successfully! Please sign in.")
        return redirect('sign_in')