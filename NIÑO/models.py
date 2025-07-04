from django.contrib.auth.models import User
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from PADRE.models import Padre
SEX_CHOICES=[('M', 'Masculino'), ('F', 'Femenino')]
ESPECIALIDAD=[('D','Disgrafia'),('T','TDA'),('DC','Discalculia')]

class ProfilePictureStorage(S3Boto3Storage):
    location = 'profile_pictures'
    default_acl = 'public-read'
    file_overwrite = False

class Niño(models.Model):
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nombres=models.CharField(max_length=100)
    apellidos=models.CharField(max_length=100)
    genero=models.CharField(max_length=1,choices=SEX_CHOICES)
    usuario=models.CharField(max_length=30)
    contraseña = models.CharField(max_length=64)
    fecha_nac=models.DateField()
    email=models.EmailField()
    foto_perfil=models.ImageField(upload_to="perfiles/", storage=ProfilePictureStorage,blank=True,null=True)
    especialidad=models.CharField(max_length=2,choices=ESPECIALIDAD)
    padre = models.ForeignKey(Padre, on_delete=models.SET_NULL, null=True, blank=True, related_name='hijos')
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def get_image(self):
        if self.foto_perfil:
            return self.foto_perfil.url

class Reporte(models.Model):
    niño = models.ForeignKey(Niño, on_delete=models.CASCADE, related_name='reportes', null=True, blank=True)
    titulo = models.CharField(max_length=100, null=True, blank=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    distracciones = models.IntegerField(null=True, blank=True, help_text="Cantidad de distracciones detectadas")
    somnolencias = models.IntegerField(null=True, blank=True)
    tiempos_somnolencia = models.JSONField(null=True, blank=True)
    tiempos_distraccion = models.JSONField(null=True, blank=True)
    frames_somnolencia = models.JSONField(null=True, blank=True)
    frames_distraccion = models.JSONField(null=True, blank=True)
    fecha = models.DateField(auto_now=True,null=True, blank=True)
    duracion_evaluacion = models.DurationField(null=True, blank=True, help_text="Duración total de la evaluación")
    comentario = models.TextField(max_length=500, null=True, blank=True)

class ProgresoNiño(models.Model):
    niño = models.OneToOneField(Niño, on_delete=models.CASCADE, related_name='progreso')
    nivel_desbloqueado = models.IntegerField(default=1)
    puntaje_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tiempo_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Progreso de {self.niño.nombre_completo}"


class ProgresoCartas(models.Model):
    niño = models.OneToOneField(Niño, on_delete=models.CASCADE)
    nivel_desbloqueado = models.IntegerField(default=1)
    puntaje_total = models.IntegerField(default=0)
    tiempo_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Progreso Cartas de {self.niño.nombre_completo}"


class ProgresoDiscalculia(models.Model):
    niño = models.OneToOneField(Niño, on_delete=models.CASCADE)
    nivel_desbloqueado = models.IntegerField(default=1)
    puntaje_total = models.IntegerField(default=0)
    tiempo_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Progreso Discalculia de {self.niño.nombre_completo}"


class PreferenciasUsuario(models.Model):
    niño = models.OneToOneField(Niño, on_delete=models.CASCADE, related_name='preferencias')
    sonido_activado = models.BooleanField(default=True)
    texto_grande = models.BooleanField(default=False)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferencias de {self.niño.nombre_completo}"
