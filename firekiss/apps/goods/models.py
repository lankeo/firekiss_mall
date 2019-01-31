from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField


# Create your models here.
class GoodsSKU(BaseModel):
    """商品SKU模型类"""
    status_choices = (
        (1, '上架'),
        (0, '下架'),
    )

    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='商品SPU')
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    brand = models.ForeignKey('GoodsBrand', on_delete=models.CASCADE, verbose_name='商品品牌')
    name = models.CharField(max_length=128, verbose_name='名称')
    desc = models.CharField(max_length=256, verbose_name='简介')
    image = models.ImageField(upload_to='goods', verbose_name='图片')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='原价')
    real_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='促销价')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价')
    integral = models.IntegerField(default=1, verbose_name='积分')
    stock = models.IntegerField(default=0, verbose_name='库存')
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态')
    # 富文本编辑器
    detail = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'fk_goods_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    """商品SPU模型类"""
    name = models.CharField(max_length=128, verbose_name='商品SPU名称')

    class Meta:
        db_table = 'fk_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    """商品图片模型类"""
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    image = models.ImageField(upload_to='goods_image', verbose_name='商品图片')

    class Meta:
        db_table = 'fk_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class GoodsProperty(BaseModel):
    """商品属性模型类"""
    # 多对多关系，
    mapp = models.ManyToManyField('GoodsSKU', through='GoodsPropMapp', through_fields=('prop', 'sku'), verbose_name='商品属性映射')
    prop_name = models.CharField(max_length=128, verbose_name='商品属性名')
    is_optional = models.BooleanField(default=True, verbose_name='是否可选')

    class Meta:
        db_table = 'fk_goods_property'
        verbose_name = '商品属性'
        verbose_name_plural = verbose_name


class GoodsPropMapp(BaseModel):
    """商品属性中间表"""
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    prop = models.ForeignKey('GoodsProperty', on_delete=models.CASCADE, verbose_name='商品属性')
    prop_value = models.CharField(max_length=256, verbose_name='商品属性值')

    class Meta:
        db_table = 'fk_goods_prop_mapp'
        verbose_name = '商品属性映射'
        verbose_name_plural = verbose_name


class GoodsType(BaseModel):
    """商品种类模型类"""
    type = models.CharField(max_length=64, verbose_name='种类')
    icon = models.CharField(max_length=20, verbose_name='种类图标', null=True)

    class Meta:
        db_table = 'fk_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name


class GoodsBrand(BaseModel):
    """商品品牌模型类"""
    brand = models.CharField(max_length=64, verbose_name='品牌')
    logo = models.ImageField(upload_to='goods_brand', verbose_name='品牌logo', null=True)

    class Meta:
        db_table = 'fk_goods_brand'
        verbose_name = '商品品牌'
        verbose_name_plural = verbose_name


class ServerPromise(BaseModel):
    """服务承诺模型类"""
    # 多对多关系，
    mapp = models.ManyToManyField('GoodsSKU', through='GoodsPromiseMapp', through_fields=('promise', 'sku'), verbose_name='商品服务承诺映射')
    promise = models.CharField(max_length=128, verbose_name='承诺')

    class Meta:
        db_table = 'fk_server_promise'
        verbose_name = '服务承诺'
        verbose_name_plural = verbose_name


class GoodsPromiseMapp(BaseModel):
    """商品服务承诺中间表"""
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    promise = models.ForeignKey('ServerPromise', on_delete=models.CASCADE, verbose_name='服务承诺')
    is_support = models.BooleanField(default=True, verbose_name='是否支持')

    class Meta:
        db_table = 'fk_goods_promise_mapp'
        verbose_name = '商品服务承诺映射'
        verbose_name_plural = verbose_name


class IndexSaleActive(BaseModel):
    """首页促销活动模型类"""
    display_area = (
        (0, '文字'),
        (1, '广告位'),
        (2, 'banner小部分'),
        (3, '首页大类banner'),
        (4, 'banner')
    )
    name = models.CharField(max_length=128, verbose_name='活动名称', null=True)
    image = models.ImageField(upload_to='index_active', verbose_name='图片', null=True)
    url = models.URLField(verbose_name='活动链接')
    display = models.SmallIntegerField(choices=display_area, verbose_name='展示区域')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'fk_index_active'
        verbose_name = '促销活动'
        verbose_name_plural = verbose_name


class IndexBrand(BaseModel):
    """首页品牌展示模型类"""
    brand = models.OneToOneField('GoodsBrand', on_delete=models.CASCADE, primary_key=True, verbose_name='品牌')
    url = models.URLField(verbose_name='品牌链接')
    index = models.SmallIntegerField(verbose_name='展示顺序')

    class Meta:
        db_table = 'fk_index_brands'
        verbose_name = '首页品牌展示'
        verbose_name_plural = verbose_name