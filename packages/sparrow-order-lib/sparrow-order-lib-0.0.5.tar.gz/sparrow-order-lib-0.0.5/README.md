# Project Description

# Release History
## version==0.0.5
############# sparrow-order-lib 使用配置 ############
export SPARROW_ORDER_APP_LABEL=sparrow_orders
export SPARROW_ORDER_AFS_APP_LABEL=sparrow_orders_afs
export SPARROW_DISTRIBUTE_APP_LABEL=sparrow_distribute
export SPARROW_AFTERSALE_APP_LABEL=sparrow_aftersale
export SPARROW_EXCHANGE_APP_LABEL=sparrow_exchange
export SPARROW_PROMOTIONS_APP_LABEL=sparrow_promotions
export SPARROW_DISSTORAGE_APP_LABEL=sparrow_disstorage
export SPARROW_PARCEL_APP_LABEL=sparrow_parcel

## version==0.0.4
将 sparrow_disstorage 维护至本项目  
新增项目 sparrow_parcel  
该版本尝试将 exceptions 维护至本项目  
```
需要新增以下环境变量
SPARROW_DISSTORAGE_APP_LABEL
SPARROW_PARCEL_APP_LABEL
```

## version==0.03
将所有公共 models 维护至本项目。
```
需要以下环境变量:  
SPARROW_ORDER_APP_LABEL
SPARROW_ORDER_AFS_APP_LABEL
SPARROW_DISTRIBUTE_APP_LABEL  
SPARROW_AFTERSALE_APP_LABEL
SPARROW_EXCHANGE_APP_LABEL
SPARROW_PROMOTIONS_APP_LABEL
```

settings 要包含以下配置
```
PHONE_NUMBER_REGEX
```

## version==0.02
测试 models 维护至 sparrow-order-lib 可行性

## version==0.01
core.db_tool.query
