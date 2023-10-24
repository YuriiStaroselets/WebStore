from django import forms
from .models import MainCategory, Category, SubCategory, Brand


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model  = MainCategory
        fields = ['main_category_name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(MainCategoryForm, self).__init__(*args, **kwargs)

        self.fields['main_category_name'].widget.attrs['placeholder'] = 'Enter Category name'
        self.fields['main_category_name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['main_category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'Enter Category discription'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['row'] = 3
        
        self.fields['image'].widget.attrs['placeholder'] = 'Add images'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['type'] = 'file'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['main_category', 'category_name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['main_category'].widget.attrs['class'] = 'form-control form-control-user'

        self.fields['category_name'].widget.attrs['placeholder'] = 'Enter Category name'
        self.fields['category_name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'Enter Category discription'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['row'] = 3

        self.fields['image'].widget.attrs['placeholder'] = 'Add images'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['type'] = 'file'


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'sub_category_name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)

        self.fields['category'].widget.attrs['class'] = 'form-control form-control-user'

        self.fields['sub_category_name'].widget.attrs['placeholder'] = 'Enter Category name'
        self.fields['sub_category_name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['sub_category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'Enter Category discription'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['row'] = 3
        
        self.fields['image'].widget.attrs['placeholder'] = 'Add images'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['type'] = 'file'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'is_displayed', 'image']

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)

        self.fields['brand_name'].widget.attrs['placeholder'] = 'Enter Brand name'
        self.fields['brand_name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['brand_name'].widget.attrs['type'] = 'text'

        self.fields['image'].widget.attrs['placeholder'] = 'Add images'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['type'] = 'file'
