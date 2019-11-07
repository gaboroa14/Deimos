@receiver(post_save,sender=Entrada)
def ImagenQR(sender, instance, **kwargs):
    if instance.qr == None:
        img = qrcode.make(instance.id)
        with open('/home/gabriel/Deimos/media/qr/' + instance.id + '.png', 'wb') as f:
            img.save(f)
        instance.qr = 'qr/' + instance.id + '.png'
        instance.save()