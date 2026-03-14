``kizuna.core.assets``
**********************

Assets and asset paths
----------------------

..  autoclass:: kizuna.core.assets.base.Asset
    :members:
    :special-members: __init__

..  autoclass:: kizuna.core.assets.paths.AssetPath
    :members:
    :special-members: __init__

..  autotype:: kizuna.core.assets.paths.AssetPathLike

..  autofunction:: kizuna.core.assets.paths.validate_asset_path


Images
------

..  autoclass:: kizuna.core.assets.image.ImageAsset
    :members:
    :special-members: __init__
    :exclude-members: on_load


Fonts
-----

..  autoclass:: kizuna.core.assets.font.FontAsset
    :members:
    :special-members: __init__
    :exclude-members: on_load

..  autodata:: kizuna.core.assets.font.DEFAULT_FONT_ASSET
