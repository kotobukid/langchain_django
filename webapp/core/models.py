from django.db import models
from pydantic import BaseModel, ValidationError, Field
from typing import List


# Pydanticを使ったスキーマ定義
class InputKeysSchema(BaseModel):
    keys: List[str]


class DesignedPrompt(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    template = models.TextField()
    input_keys = models.JSONField(verbose_name="キー名 ([\"name\", \"age\"])")

    class Meta:
        verbose_name = "プロンプトテンプレート"
        verbose_name_plural = "プロンプトテンプレート"

    def __str__(self):
        return self.name

    def clean(self):
        """保存前にJSONフィールドをバリデーション"""
        super().clean()

        print(self.input_keys)

        try:
            # Pydanticスキーマを使ってバリデーション
            InputKeysSchema(keys=self.input_keys)
        except ValidationError as e:
            # バリデーションエラーの場合、例外を投げる
            raise models.ValidationError(f"Invalid input keys: {e}")
