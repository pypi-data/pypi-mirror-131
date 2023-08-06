from ..core.constants import ShippingPartnerCodes as Partner

PARCEL_ERROR_CODE_PREFIX = 249000


class ParcelStatus:
    """ 包裹状态 """
    INIT = 'init'  # 初始   待上架
    CANCEL = 'cancel'  # 取消打包
    CHECKING = 'checking'  # 上架待揽收
    CHECKED = 'checked'  # 已揽收


class TransferStatus:
    """ 交接记录状态 """
    ACTIVE = "active"  # 已上架
    INACTIVE = 'inactive'  # 已召回


class ExpressName:
    """ 包裹管理中给前端用的快递公司 """

    SF = 'sf'
    YZ = 'yz'

    CODE_2_system_codes = {
        SF: [Partner.SF, Partner.SFTCJS],
        YZ: [Partner.YZPY]
    }

    CODE_2_NAME_MAP = {
        SF: "顺丰",
        YZ: "邮政",
    }

    EXPRESS_NAME_INFOS = [
        {
            "name": CODE_2_NAME_MAP[SF],
            "code": SF,
        },
        {
            "name": CODE_2_NAME_MAP[YZ],
            "code": YZ,
        },
    ]
