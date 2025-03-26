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


class GenerationHistory(models.Model):
    prompt = models.ForeignKey(DesignedPrompt, on_delete=models.CASCADE)
    context_object = models.JSONField()
    style = models.CharField(max_length=16, default="default")
    generated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.pk}] {self.prompt.name} / {self.style} ({self.context_summary()})"

    def context_summary(self):
        return ", ".join(self.context_object.values())

    class Meta:
        verbose_name = "生成履歴"
        verbose_name_plural = "生成履歴"
