from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
    
def crop_max_square(theme_obj, thumb_width):
    pil_img = Image.open(theme_obj.image)
    pil_img = pil_img.convert('RGB')
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size)).resize((thumb_width, thumb_width), Image.LANCZOS)

# this function triggers when 'Theme' model saved
# this method is not used here, the algorithm has been changed
def image_save_trigger(new_theme):
    user = new_theme.author
    img_to_convert = new_theme
    thumb_width = 500
    img_squared = crop_max_square(img_to_convert, thumb_width)
    thumb_io = BytesIO()
    img_squared.save(thumb_io, format='JPEG')
    new_name = f"{new_theme.title}-{new_theme.pk}-{user.pk}.jpg"
    thumb_file = InMemoryUploadedFile(thumb_io, None, new_name, 'image/jpeg',
                            thumb_io.tell, None)
    new_theme.image = thumb_file


def image_resizer(theme_object):
    #image resizing
    foo = Image.open(theme_object.image.path)
    width, height = foo.size
    TARGET_WIDTH = 500
    coefficient = width / 500
    new_height = height / coefficient
    foo = foo.resize((int(TARGET_WIDTH),int(new_height)),Image.ANTIALIAS)
    foo.save(theme_object.image.path,quality=50)
    return True
    
    
#convert string to integer
def str_to_int(string):
    try: return int(string)
    except: return False 


# return user object or False
def get_user(request):
    if str(request.user) != "AnonymousUser": 
        return request.user
    else: return False 


#returns string for html
def member_for(date_joined) -> str:
    try:
        now = datetime.now()
        diff = (now.year - date_joined.year) * 12 + (now.month  - date_joined.month )
        return f"Member for {diff} months"
    except: return f"Member for 0 months"