from io import BytesIO
from pathlib import Path

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models

from users.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_image = models.ImageField(upload_to='todo/completed_images/', null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails/',
        null=True,
        blank=True,
        default='todo/no_image/no_image.jpeg'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 기존 객체 불러오기 (update인지 확인)
        is_update = self.pk is not None
        old_image_path = None

        if is_update:
            try:
                old = Todo.objects.get(pk=self.pk)
                if (
                    old.completed_image
                    and old.completed_image.name != self.completed_image.name
                ):
                    old_image_path = old.completed_image.path
            except Todo.DoesNotExist:
                pass

        # 먼저 기본 저장
        super().save(*args, **kwargs)

        # 새 이미지가 있거나, 기존 이미지가 바뀌었으면 썸네일 생성
        if self.completed_image and (not self.thumbnail or old_image_path):
            try:
                img = Image.open(self.completed_image)
                img.thumbnail((200, 200))

                img_path = Path(self.completed_image.name)
                stem = img_path.stem
                suffix = img_path.suffix.lower()

                ext_map = {
                    ".jpg": "JPEG",
                    ".jpeg": "JPEG",
                    ".png": "PNG",
                    ".gif": "GIF",
                }

                file_type = ext_map.get(suffix)
                if not file_type:
                    return

                thumb_name = f"{stem}_thumb{suffix}"

                temp_thumb = BytesIO()
                img.save(temp_thumb, format=file_type)
                temp_thumb.seek(0)

                self.thumbnail.save(
                    thumb_name, ContentFile(temp_thumb.read()), save=False
                )
                temp_thumb.close()

                # 최종 저장
                super().save(*args, **kwargs)

            except Exception as e:
                print(f"[썸네일 생성 오류] {e}")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.message}'
