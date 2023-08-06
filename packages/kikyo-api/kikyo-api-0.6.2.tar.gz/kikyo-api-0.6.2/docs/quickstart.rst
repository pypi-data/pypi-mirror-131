.. _quickstart:

快速上手
================================================================================

准备工作
--------------------------------------------------------------------------------

首先，我们需要初始化连接数据统一接入平台的客户端，示例如下：

.. code-block:: python

    from kikyo_api import KikyoClient

    endpoint = '<kikyo endpoint>'
    username = '<your username>'
    password = '<your password>'

    kikyo_client = KikyoClient(endpoint, username=username, password=password)


``endpoint`` 表示数据统一接入平台的服务地址，在不同环境下的取值如下表所示：

.. csv-table::
   :header: 环境名称, endpoint
   :widths: 100, 300

   所内, kikyo.app.kdsec.org
   大工程, kikyo.app.kdsec.org

用户名和密码请联系管理员获取。

之后，我们便可以基于 ``kikyo_client`` 使用统一数据接入平台提供的各项能力。
