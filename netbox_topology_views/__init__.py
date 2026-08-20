from netbox.plugins import PluginConfig


class TopologyViewsConfig(PluginConfig):
    name = "netbox_topology_views"
    verbose_name = '网络拓扑视图'
    description = '网络拓扑可视化插件'
    version = "4.5.1"
    author = "Mattijs Vanhaverbeke"
    author_email = "author@example.com"
    base_url = "netbox_topology_views"
    required_settings = []
    default_settings = {
        "static_image_directory": "netbox_topology_views/img",
        # Fix: enable coordinate saving out of the box so the drag-to-fix
        # layout feature works without requiring a manual PLUGINS_CONFIG entry.
        "allow_coordinates_saving": True,
        "always_save_coordinates": False,
    }

    def ready(self):
        from . import signals

        super().ready()


config = TopologyViewsConfig
