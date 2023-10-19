
from django import forms
from ads.models import Ad, Comment
from django.core.files.uploadedfile import InMemoryUploadedFile
from ads.humanize import naturalsize


# Create the form class.
class AdCreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024 # 2MB
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+str(max_upload_limit_text))
    upload_field_name = 'picture'

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Ad
        fields = ['title', 'price', 'text','tags', 'picture']  # Picture is manual(because it is not ImageField)

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return cleaned_data
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit+" bytes")
        return cleaned_data
    # Convert uploaded File object to a picture
    def save(self, commit=True):
        model_instance = super().save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = model_instance.picture
        if isinstance(f, InMemoryUploadedFile):  # if the image data is in memory and not in file sys that means it is fresh
            bytearr = f.read()
            model_instance.content_type = f.content_type
            model_instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            model_instance.save()
            self.save_m2m()
        return model_instance
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='Comments',
        widget=forms.TextInput(attrs={'placeholder': 'Add your comment here...'})
    )
    
    class Meta:
        model = Comment
        fields = ['text']

