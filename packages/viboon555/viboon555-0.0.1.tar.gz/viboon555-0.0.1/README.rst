(Viboon Profile) เป็นตัวอย่างการอัปโหลด package ไปยัง PyPi
==========================================================

PyPi: https://pypi.org/project/viboon555/

สวัสดีครับ Package นี้เป็นแพ็คเก็จ ที่อธิยาย Profile ของนาย วิบูลย์
ปานแก้ว สามารถนำไปใช้กับผู้อื่นได้

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install viboon555

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   my = Profile('Viboon')
   my.company = 'GGG'
   my.hobby = ['วาดภาพ','Reading','Sleep']
   my.sport = ['ฟุตบอล','Boxing','Hose']
   print(my.name)
   my.show_email()
   my.show_myart()
   my.show_hobby()
   my.show_sport()

พัฒนาโดย: นาย วิบูลย์ ปานแก้ว FB: https://www.facebook.com/li.dxngpu
