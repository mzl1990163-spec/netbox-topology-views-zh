from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

coordinategroup_buttons = (
    PluginMenuButton(
        link='plugins:netbox_topology_views:coordinategroup_add',
        title='新建',
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_topology_views.add_coordinategroup']
    ),
    PluginMenuButton(
        link='plugins:netbox_topology_views:coordinategroup_import',
        title='导入',
        icon_class='mdi mdi-upload',
        permissions=['netbox_topology_views.add_coordinategroup']
    )
)

circuitcoordinate_buttons = (
    PluginMenuButton(
        link='plugins:netbox_topology_views:circuitcoordinate_add',
        title='新建',
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_topology_views.add_coordinate']
    ),
    PluginMenuButton(
        link='plugins:netbox_topology_views:circuitcoordinate_import',
        title='导入',
        icon_class='mdi mdi-upload',
        permissions=['netbox_topology_views.add_coordinate']
    )
)

powerpanelcoordinate_buttons = (
    PluginMenuButton(
        link='plugins:netbox_topology_views:powerpanelcoordinate_add',
        title='新建',
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_topology_views.add_coordinate']
    ),
    PluginMenuButton(
        link='plugins:netbox_topology_views:powerpanelcoordinate_import',
        title='导入',
        icon_class='mdi mdi-upload',
        permissions=['netbox_topology_views.add_coordinate']
    )
)

powerfeedcoordinate_buttons = (
    PluginMenuButton(
        link='plugins:netbox_topology_views:powerfeedcoordinate_add',
        title='新建',
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_topology_views.add_coordinate']
    ),
    PluginMenuButton(
        link='plugins:netbox_topology_views:powerfeedcoordinate_import',
        title='导入',
        icon_class='mdi mdi-upload',
        permissions=['netbox_topology_views.add_coordinate']
    )
)

coordinate_buttons = (
    PluginMenuButton(
        link='plugins:netbox_topology_views:coordinate_add',
        title='新建',
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_topology_views.add_coordinate']
    ),
    PluginMenuButton(
        link='plugins:netbox_topology_views:coordinate_import',
        title='导入',
        icon_class='mdi mdi-upload',
        permissions=['netbox_topology_views.add_coordinate']
    )
)

menu = PluginMenu(
    label='网络拓扑',
    icon_class="mdi mdi-sitemap",
    groups=(
        ('拓扑', 
            (
                PluginMenuItem(link="plugins:netbox_topology_views:home", link_text="实时拓扑", permissions=["dcim.view_site", "dcim.view_device"]),
                PluginMenuItem(link="plugins:netbox_topology_views:saved_filters", link_text="我的拓扑", permissions=["dcim.view_site", "dcim.view_device"]),
            ),
        ),
        ('坐标', 
            (
                PluginMenuItem(link="plugins:netbox_topology_views:coordinategroup_list", link_text="坐标组", buttons=coordinategroup_buttons, permissions=['netbox_topology_views.view_coordinategroup']),
                PluginMenuItem(link="plugins:netbox_topology_views:coordinate_list", link_text="设备坐标", buttons=coordinate_buttons, permissions=['netbox_topology_views.view_coordinate']),
                PluginMenuItem(link="plugins:netbox_topology_views:powerfeedcoordinate_list", link_text="电源馈线坐标", buttons=powerfeedcoordinate_buttons, permissions=['netbox_topology_views.view_coordinate']),
                PluginMenuItem(link="plugins:netbox_topology_views:powerpanelcoordinate_list", link_text="配电盘坐标", buttons=powerpanelcoordinate_buttons, permissions=['netbox_topology_views.view_coordinate']),
                PluginMenuItem(link="plugins:netbox_topology_views:circuitcoordinate_list", link_text="电路坐标", buttons=circuitcoordinate_buttons, permissions=['netbox_topology_views.view_coordinate']),
            ),
        ),
        ('偏好设置', 
            (
                PluginMenuItem(link="plugins:netbox_topology_views:images", link_text="图标配置", permissions=[ "dcim.view_site","dcim.view_devicerole"]),
                PluginMenuItem(link="plugins:netbox_topology_views:individualoptions", link_text="个性化选项", permissions=['netbox_topology_views.change_individualoptions']),
            ),
        ),
    ),
)
