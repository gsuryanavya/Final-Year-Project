from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserImageForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth import authenticate,login,logout
from .models import UserImageModel
import numpy as np
from tensorflow import keras
from PIL import Image,ImageOps

import pyttsx3
import time


def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

from .models import Profile

def profile(request):
    user = request.user
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from . models import UserImageModel
from . import forms
from .forms import UserImageForm


def Deploy_8(request): 
    print("HI")
    if request.method == "POST":
        form = forms.UserImageForm(files=request.FILES)
        if form.is_valid():
            print('HIFORM')
            form.save()
        obj = form.instance

        result1 = UserImageModel.objects.latest('id')
        models = keras.models.load_model('C:/Users/91908/Music/FETAL HEALTH/FETAL HEALTH/CODING/Deploy/Project/App/keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open("C:/Users/91908/Music/FETAL HEALTH/FETAL HEALTH/CODING/Deploy/Project/media/" + str(result1)).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        classes = ["Non-standard","Standard"]
        prediction = models.predict(data)
        idd = np.argmax(prediction)
        a = (classes[idd])
        if a == "Non-standard":
            b ='This Image Detected Non-standard'
        elif a == "Standard":
            b ='This Image Detected Standard'
        

        else:
            b = 'WRONG INPUT'

        data = UserImageModel.objects.latest('id')
        data.label = a
        data.save()

        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 10)  # Decrease rate by 50 (default rate is typically around 200)
        engine.say(a)
        engine.runAndWait()

        
        # text_to_speech(a, delay=7)

        
        return render(request, 'App/output.html',{'form':form,'obj':obj,'predict':a, 'predicted':b})
    else:
        
        form = forms.UserImageForm()
    return render(request, 'App/model.html',{'form':form})

import joblib

Model = joblib.load('C:/Users/91908/Music/FETAL HEALTH/FETAL HEALTH/CODING/Deploy/Project/App/FETAL1.pkl')

from .forms import FetalHealth_form
from .models import FetalHealthData
    


def Deploy_9(request): 
    form = FetalHealth_form()  # Initialize the form outside the if block
    
    if request.method == 'POST':
        
            form = FetalHealth_form(request.POST)
            if form.is_valid():
                # Extract cleaned data from form
                LBE = form.cleaned_data['LBE']
                LB = form.cleaned_data['LB']
                AC = form.cleaned_data['AC']
                FM = form.cleaned_data['FM']
                UC = form.cleaned_data['UC']
                ASTV = form.cleaned_data['ASTV']
                MSTV = form.cleaned_data['MSTV']
                ALTV = form.cleaned_data['ALTV']
                MLTV = form.cleaned_data['MLTV']
                DL = form.cleaned_data['DL']
                DS = form.cleaned_data['DS']
                DP = form.cleaned_data['DP']
                DR = form.cleaned_data['DR']
                Width = form.cleaned_data['Width']
                Min = form.cleaned_data['Min']
                Max = form.cleaned_data['Max']
                Nmax = form.cleaned_data['Nmax']
                Nzeros = form.cleaned_data['Nzeros']
                Mode = form.cleaned_data['Mode']
                Mean = form.cleaned_data['Mean']
                Median = form.cleaned_data['Median']
                Variance = form.cleaned_data['Variance']
                Tendency = form.cleaned_data['Tendency']
                SUSP = form.cleaned_data['SUSP']
                CLASS = form.cleaned_data['CLASS']
                
                # Prepare features for prediction
                features = np.array([[LBE, LB, AC, FM, UC, ASTV, MSTV, ALTV, MLTV, DL, DS, DP, DR,
                                    Width, Min, Max, Nmax, Nzeros, Mode, Mean, Median, Variance,
                                    Tendency,SUSP, CLASS]])
                
                # Reshape features to be 2-dimensional
                features = features.reshape(1, -1)
                
                # Predict using the loaded model (assuming 'Model' is your trained model)
                prediction = Model.predict(features)
                prediction = prediction[0]  # Extract the predicted class label
                
                # Determine human-readable label
                if prediction == 1:
                    a = 'Normal'
                elif prediction == 2:
                    a = 'Suspicious'
                elif prediction == 3 :
                    a = 'Pathological'
                
                # Save data to database
                instance = form.save(commit=False)
                instance.label = a
                instance.save()
                
                print('data saved')
                
                return render(request, 'app/Ml_output.html', {"predict": a})
            else:
                print('Form is not valid')
            
    return render(request, 'app/9_Deploy.html', {"form": form})

def ML_DB(request):
    predictions = FetalHealthData.objects.all()
    return render(request, 'App/ML_DB.html', {'predictions':predictions })

def Basic(request):
    return render(request,'App/Basic_report.html')

def Metrics(request):
    return render(request,'App/Metrics_report.html')

def Database(request):
    models = UserImageModel.objects.all()
    return render(request, 'App/Database.html', {'models': models})


def logout_view(request):  
    auth_logout(request)
    return redirect('/')

from django.shortcuts import render
from .models import Profile

def profile_list(request):
    # Fetch all profile objects from the database
    profiles = Profile.objects.all()
    
    # Pass the profiles data to the template
    return render(request, 'app/profile_list.html', {'profiles': profiles})
