from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

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
            'form': form,
            'step': step,
            'total_steps': len(FORMS),
            'progress_percentage': int(((step - 1) / len(FORMS)) * 100)
        }
        return render(request, TEMPLATE, context)

    def post(self, request):
        step = int(request.POST.get('step', 1))

        # Navigate to previous step
        if 'prev_step' in request.POST:
            prev_step = step - 1
            return redirect(f"{reverse('sign_up')}?step={prev_step}")

        # Skip current step
        if 'skip_step' in request.POST:
            signup_data = request.session.get('signup_data', {})
            signup_data[f'step_{step}'] = {}
            request.session['signup_data'] = signup_data

            if step == len(FORMS):
                return self.complete_signup(request)
            else:
                next_step = step + 1
                return redirect(f"{reverse('sign_up')}?step={next_step}")

        # Load form
        try:
            form_class = FORMS[step - 1][1]
            form = form_class(request.POST, request.FILES)
        except IndexError:
            return redirect(reverse('sign_up'))

        if form.is_valid():
            signup_data = request.session.get('signup_data', {})

            # ----------------------
            # STEP 1: Create Account
            # ----------------------
            if step == 1:
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                full_name = form.cleaned_data.get('full_name')

                if Account.objects.filter(email=email).exists():
                    messages.error(request, "This email address is already in use.")
                    del request.session['signup_data']
                    return redirect('sign_up')

                try:
                    with transaction.atomic():
                        new_account = Account.objects.create_user(
                            email=email,
                            password=password
                        )
                        AccountDetail.objects.create(
                            account=new_account,
                            name=full_name
                        )

                        # Save account_id in session for later steps
                        signup_data['account_id'] = str(new_account.id)
                        signup_data[f'step_{step}'] = form.cleaned_data
                        request.session['signup_data'] = signup_data

                except Exception as e:
                    messages.error(request, "Unexpected error during account creation.")
                    return redirect('sign_up')

                # Move to next step
                next_step = step + 1
                return redirect(f"{reverse('sign_up')}?step={next_step}")

            # ----------------------
            # STEP 2 & 3: Update AccountDetail
            # ----------------------
            else:
                account_id = signup_data.get('account_id')
                if not account_id:
                    messages.error(request, "Something went wrong. Please start over.")
                    return redirect('sign_up')

                try:
                    account_detail = AccountDetail.objects.get(account_id=account_id)
                    for key, value in form.cleaned_data.items():
                        if hasattr(account_detail, key):
                            setattr(account_detail, key, value)
                    account_detail.save()

                    signup_data[f'step_{step}'] = form.cleaned_data
                    request.session['signup_data'] = signup_data

                except AccountDetail.DoesNotExist:
                    messages.error(request, "Account details not found. Please start over.")
                    return redirect('sign_up')

                # If last step, complete signup
                if step == len(FORMS):
                    return self.complete_signup(request)
                else:
                    next_step = step + 1
                    return redirect(f"{reverse('sign_up')}?step={next_step}")

        # Form invalid: render with errors
        context = {
            'form': form,
            'step': step,
            'total_steps': len(FORMS),
            'progress_percentage': int(((step - 1) / len(FORMS)) * 100)
        }
        return render(request, TEMPLATE, context)

    # ----------------------
    # Complete Signup
    # ----------------------
    def complete_signup(self, request):
        signup_data = request.session.get('signup_data', {})
        account_id = signup_data.get('account_id')

        if not account_id:
            messages.error(request, "Something went wrong. Please start over.")
            return redirect('sign_up')

        # Log signup success
        access_log_service.save_log(
            AccessLogForm.sing_up_success_form(),
            account_id
        )

        # Clear session
        del request.session['signup_data']
        messages.success(request, "Your account has been created successfully! Please sign in.")
        return redirect('sign_in')
