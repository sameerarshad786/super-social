from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from post.models.postremark_model import PostRemark


class PostRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRemark
        fields = ("popularity", "on_post", "user")
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        on_post = validated_data.get("on_post")
        user = self.context["request"].user
        if PostRemark.objects.filter(user=user, on_post=on_post).exists():
            raise exceptions.Throttled(_("Entry already created"))
        return PostRemark.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user == instance.user:
            return super().update(instance, validated_data)
        raise exceptions.PermissionDenied(_(
            "403 forbidden"
        ))