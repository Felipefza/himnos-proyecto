from apiHimnos.models import Parrafos

parrafos = Parrafos.objects.all()
index: int = 1
himno_id: int = 1

for item in parrafos:
    if item.himno_id_fk == himno_id:
        item.numero_index = index
        index += 1

    else:
        index = 1
        himno_id = item.himno_id_fk
        item.numero_index = index
        index += 1

    item.save()
