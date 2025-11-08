from rest_framework import serializers
<<<<<<< HEAD
from common.models import Attendance, Student , Grade
=======
from common.models import Attendance, Student
>>>>>>> 82e4ca92702e200abb25ae916d02cb5601e1fa5f


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "full_name", "phone", "group"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "student", "group", "date_time", "is_present"]

<<<<<<< HEAD
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
=======

>>>>>>> 82e4ca92702e200abb25ae916d02cb5601e1fa5f
