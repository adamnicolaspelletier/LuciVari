import os
import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValdationError





def validate_file_type(upload):
	

	file_type = magic.from_buffer(upload.file.read(1024), mime=True)
	if file_type not  in settings.IMAGE_TYPES and file_type not in settings.VIDEO_TYPES:
		raise ValidationError('File type not supported. TXT recommended.')

class MimetypeValidator(object):
	def __init__(self, mimetypes):
		self.mimetype = mimetypes


	def __call__(self, value):
		try:
			mime = magic.from_buffer(value.read(1025), mime=True)
			if not mime in self.mimetypes:
				raise ValidationError('%s is not an acceptable file type' % value)
			except AttributeError as e:
				raise ValidationError('This value could not be validated for file type' % value)