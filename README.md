# QueraPyRate
Quera Final Project

## Manifest

### Commit rule:

*   Start commit with \[add\] ,\[modify\], \[fix\]
*   Comment
*   Description (Optional)

```plaintext
[Add] Comment

Description
```

### Branch Rule:

#### Branch name:

*   main → for ci/cd
*   hotfix -- for fix bug in main branch
*   release → for release tag
*   develop → second main branch, all below branch merge from this branch
*   feature → for each feature
    *   feature/feature\_name
    *   feature/feautre\_name2
*   bugfix → for each bug in develop branch
    *   bugfix/bug\_name
    *   bugfix/bug\_name2

#### Rule:

*   Start new branch, then Sync branch with `develop` branch
*   Commit and push code every day
*   When finishing the task and pushed to origin then `pull request` to `develop` branch
*   Review `pull request` merge to `develop` branch
*   ~If Task finished and~ `~develop~` ~branch not sync, then merge~ `~develop~` ~into the in progress, and fix the conflict.~

### Code:

#### Import:

```plaintext
from django.contrib.auth.models import AbstractUser, Aliuser, FUser
--->
from django.contrib.auth import  models as user_models 

class User(user_models.AbstractUser)

from package_name import forms as package_name_forms
from package_name import models as package_name_models
from package_name import views as package_name_views
from package_name import serializers as package_name_serializers
```

#### Urls:

*   add urls to each app and include urls `project file`

```plaintext
package_name/urls.py
urlpatterns = [
path(....,view,name=...),
path(....,view,name=...),
]

project_name/urls.py
urlpatterns = [
path(....,include,name=...),
path(....,include,name=...),
]
```

#### Query:

*   `ObjectManager`
*   all queries in object manager

```plaintext
class QuestionManager(models.Manager):
    def get_x_by_y(self, user):
        return self.filter(user=user)
    

class Question(models.Model):
	varibales
		
    objects = QuestionManager()

	@propery
	
	other functions
```

### Models Relation:

*   `ForeignKey`
*   `OneToOneField`

```plaintext
models.ForeignKey('package_name.model',)
models.OneToOneField('package.model',)
```

*   `on_delete=models.PROTECT`
*   `verbose_name`:  create `varaible_name.py` file

```plaintext
# User
USERNAME = 'نام کاربری'
FIRST_NAME = 'نام'
LAST_NAME = 'نام خانوادگی'

# Answer field
ANSWER_USER = 'کاربر ایجاد کننده'
UPVOTERS = 'نظر مثبت'
```

#### Comment:

*   Each class, function → doc string

```plaintext
class Answer(models.Model):
    """
    توضیح برای کلاس
    
    """
   
```