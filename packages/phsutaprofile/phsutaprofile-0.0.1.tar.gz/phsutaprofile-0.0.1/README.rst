(Phsuta Profile) เป็นตัวอย่างในการ upload package ไป Pypi.org
=============================================================

PyPi: https://pypi.org/project/phsutaprofile/

สวัสดี package นี้มีไว้เพื่ออธิบาย profile ของ Tony และสามารถนำไปใช้กับ
user อื่นได้

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install phsutaprofile

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   my = Profile('Tony')
   my.company = 'Phsuta'
   my.hobby = ['Developer','Programming','Reading','Diving']
   print(my.name)
   my.show_email()
   my.show_myart()
   my.show_hobby()

Developed By B1ackmonday
