from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    completed_image = models.ImageField(upload_to='completed_images/', null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        default='defaults/default_thumb.jpg'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.completed_image and not self.thumbnail:
            try:
                img = Image.open(self.completed_image)
                img.thumbnail((200, 200))

                # 이미지 경로 처리
                img_path = Path(self.completed_image.name)
                stem = img_path.stem
                suffix = img_path.suffix.lower()
                file_type = "JPEG" if suffix in [".jpg", ".jpeg"] else "PNG"

                # 썸네일 파일명
                thumb_name = f"{stem}_thumb{suffix}"

                # 메모리에 임시 파일 저장
                temp_thumb = BytesIO()
                img.save(temp_thumb, file_type)
                temp_thumb.seek(0)

                # 파일 저장
                self.thumbnail.save(
                    thumb_name, ContentFile(temp_thumb.read()), save=False
                )
                temp_thumb.close()

                # 객체 최종 저장
                super().save(update_fields=["thumbnail"])
            except Exception as e:
                print(f"[Thumbnail Error] {e}")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
