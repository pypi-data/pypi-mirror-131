.. _data_topics:

数据主题
================================================================================

.. note::
   更多的字段信息请参考实际的数据内容。


境外新闻
--------------------------------------------------------------------------------

- **topic名称** : ``origin.overseas_news``
- **支持环境** : 所内

.. csv-table::
   :header: 字段名称, 类型, 描述, 备注
   :widths: 100, 50, 300, 200

   url, str, 新闻地址,
   hash, str, 新闻地址的哈希值,
   source, str, 数据源名称,
   title, str, 新闻标题,
   content, str, 新闻内容,
   websiteName, str, 网站名称,


Telegram群组消息
--------------------------------------------------------------------------------

- **topic名称** : ``origin.tg_msg``
- **支持环境** : 所内

.. csv-table::
   :header: 字段名称, 类型, 描述, 备注
   :widths: 100, 50, 300, 200

   message_id, int, 消息id,
   chat_id, int, 群组id,
   caption, str, 消息内容,


Telegram新闻
--------------------------------------------------------------------------------

- **topic名称** : ``origin.tg_news``
- **支持环境** : 所内

.. csv-table::
   :header: 字段名称, 类型, 描述, 备注
   :widths: 100, 50, 300, 200

   message_id, int, 消息id,
   chat_id, int, 群组id,
   news_id, str, 新闻id,
   title, str, 新闻标题,
   content, str, 新闻内容,
   file_names, List[str], 新闻中的文件名称, 文件位于 ``news-files`` bucket中
