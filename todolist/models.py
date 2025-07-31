from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models


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
        # 객체가 이미 존재하는 경우 (update)
        if self.pk:
            old = Todo.objects.get(pk=self.pk)
            image_changed = old.completed_image != self.completed_image
        else:
            image_changed = False

        # 먼저 기본 저장
        super().save(*args, **kwargs)

        # 조건: 이미지가 존재하고 썸네일이 없거나 이미지가 바뀌었을 경우만 생성
        if self.completed_image and (not self.thumbnail or image_changed):
            try:
                img = Image.open(self.completed_image)
                img.thumbnail((200, 200))

                # 이미지 경로 처리
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
                    return  # 지원하지 않는 포맷이면 종료

                # 썸네일 파일명 생성
                thumb_name = f"{stem}_thumb{suffix}"

                # 메모리에 임시 저장
                temp_thumb = BytesIO()
                img.save(temp_thumb, format=file_type)
                temp_thumb.seek(0)

                # 썸네일 필드에 저장
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
