# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from asuntosParticulares.views.enums import EstadoSolicitud

def enviar_resolucion_email(resolucion, user_email, buffer_documento=None):

    resolucion = str(resolucion)
    user_email = str(user_email)
    
    if resolucion.startswith("EstadoSolicitud."):
        nombre_enum = resolucion.split('.')[-1]
        estado = EstadoSolicitud[nombre_enum]
    else:
        estado = EstadoSolicitud(resolucion)

    
    subject = 'Resolución día de asuntos propios'
    html_message = ""
    # Tu lógica para definir el mensaje HTML no cambia
    if estado == EstadoSolicitud.CONCEDER_PRIMER:
        html_message = '<div style="color: black;"><p>Buenos días,</p><p>Adjunto te doy traslado de la resolución acerca de tu solicitud del permiso por asuntos particulares, de acuerdo con la ORDEN de 29 de agosto de 2024.</p> Es importante tener en cuenta que, en caso de coincidir con evaluaciones o reuniones del período de reclamaciones, la concesión del permiso se considerará revocada.</p><p>Cabe recordar que el procedimiento de concesión de días de asuntos propios del Centro establece prioridad sobre el primer día solicitado por parte del profesorado interesado, a partir del cual, el resto de concesiones se supedita a que no exista profesorado de primera demanda que requiera dicha fecha. En cualquier caso, la concesión actual será definitiva con un mes de antelación, si no ha existido exceso de demanda.</p><p>Si esta concesión obedece a causas sobrevenidas, deberá constar la documentación justificativa pertinente.</p><p>Un saludo.</p></div>'
    elif estado == EstadoSolicitud.CONCEDER:
        html_message = '<div style="color: black;"><p>Buenos días,</p><p>Adjunto te doy traslado de la resolución acerca de tu solicitud del permiso por asuntos particulares, de acuerdo con la ORDEN de 29 de agosto de 2024.</p><p>Al tratarse de una segunda o sucesiva petición, cabe recordar que el procedimiento de concesión de días de asuntos propios del Centro establece prioridad sobre el primer día solicitado por parte del profesorado interesado, a partir del cual, el resto de concesiones se supedita a que no exista profesorado de primera demanda que requiera dicha fecha.</p> <p><strong>En cualquier caso, la concesión actual será definitiva con un mes de antelación, si no ha existido exceso de demanda.</strong></p><p>Si existen peticiones posteriores a esta fecha de profesorado que aún no ha disfrutado de dichos días, antes del mes definitivo, se comunicará al profesorado interesado que el derecho original decae, por razones de organización del servicio.</p><p>Si esta concesión obedece a causas sobrevenidas, deberá constar la documentación justificativa pertinente.</p><p>Un saludo.</p></div>'
    elif estado == EstadoSolicitud.DENEGAR:
        html_message = '<div style="color: black;"><p>Buenos días,</p><p>Te doy traslado de la resolución acerca de tu solicitud del permiso por asuntos particulares, de acuerdo con la ORDEN de 29 de agosto de 2024.</p><p><strong>No puede atenderse la petición, por razones de servicio, número de solicitudes</strong> y para garantizar el funcionamiento del Centro. Por lo tanto, quedas en lista de espera, por si existiesen renuncias o bajas para la citada fecha.</p><p>Cabe recordar que el procedimiento de concesión de días de asuntos propios del Centro establece prioridad sobre el primer día solicitado por parte del profesorado interesado, a partir del cual, el resto de concesiones se supedita a que no exista profesorado de primera demanda que requiera dicha fecha. En cualquier caso, la concesión actual será definitiva con un mes de antelación, si no ha existido exceso de demanda.</p><p>Un saludo.</p></div>'
    elif estado == EstadoSolicitud.DENEGAR_15:
        html_message = '<div style="color: black;"><p>Buenas tardes,</p><p>La petición del permiso por asuntos particulares, según la ORDEN de 29 de agosto de 2024, indica, en su Artículo 13, permiso por asuntos particulares, lo siguiente:</p><p style="font-style:italic;">5. La solicitud debe efectuarse con una <strong>antelación</strong> mínima, con carácter general, de <strong>quince días naturales respecto a la fecha prevista para su disfrute</strong>, salvo <strong>circunstancias sobrevenidas</strong> en las que no se haya podido prever la necesidad del día de asuntos particulares. La <strong>circunstancia sobrevenida ha de ser justificada</strong> y, excepcionalmente, se podrá presentar una <strong>declaración responsable.</strong> El plazo máximo de presentación de solicitudes será de tres meses de antelación a la fecha del disfrute.</p><p>Entendiendo que puede darse esta circunstancia en la petición del día , dejo bloqueado el día a la espera de la justificación, para su posterior concesión.</p><p>Un saludo.</p></div>'
    else:
        # Si no hay una resolución válida, no hacemos nada
        return

    # Creamos una versión del mensaje en texto plano
    plain_message = strip_tags(html_message)
    
    # 2. Llamamos a la función de Django correctamente
    email = EmailMultiAlternatives(
        subject,
        plain_message, # Mensaje en texto plano
        settings.EMAIL_HOST_USER, # Remitente desde settings
        [user_email],
        #html_message=html_message, # Mensaje en formato HTML
    )
    email.attach_alternative(html_message, "text/html")
    
    # 3. Adjuntar el fichero desde el buffer
    email.attach(
        'Resolucion.docx',  # Nombre que tendrá el fichero adjunto
        buffer_documento.getvalue(),  # Contenido del fichero desde el buffer
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # MIME type para .docx
    )
    
    try:
        email.send()
    except Exception as e:
        pass