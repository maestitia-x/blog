< !-- PAGINATION
KONTROLLER -->
{ % if posts.has_other_pages %}
< div
style = "text-align: center; margin-top: 3rem; display: flex; gap: 1rem; justify-content: center; align-items: center;" >

< !-- Önceki
Butonu -->
{ % if posts.??? %}
< a
href = "?page={{ posts.??? }}"
style = "background: #2196F3; color: white; padding: 0.8rem 1.5rem; text-decoration: none; border-radius: 5px;" >
← Önceki
< / a >
{ % endif %}

< !-- Sayfa
Bilgisi -->
< span
style = "color: #666;" >
Sayfa
{{posts.???}} / {{posts.paginator.???}}
< / span >

< !-- Sonraki
Butonu -->
{ % if posts.??? %}
< a
href = "?page={{ posts.??? }}"
style = "background: #2196F3; color: white; padding: 0.8rem 1.5rem; text-decoration: none; border-radius: 5px;" >
Sonraki →
< / a >
{ % endif %}

< / div >
{ % endif %}
