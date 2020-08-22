# coding: utf-8
from __future__ import unicode_literals


item_insert = [
    'item.itemUrl',
    'item.itemNumber',
    'item.itemName',
    'item.itemPrice',
    'item.genreId',
    'item.catalogId',
    'item.catalogIdExemptionReason',
    'item.images',
    'item.images.image',
    'item.images.image.imageUrl',
    'item.images.image.imageAlt',
    'item.descriptionForPC',
    'item.descriptionForMobile',
    'item.descriptionForSmartPhone',
    'item.movieUrl',
    'item.options',
    'item.options.option',
    'item.options.option.optionName',
    'item.options.option.optionStyle',
    'item.options.option.optionValues',
    'item.options.option.optionValues.optionValue',
    'item.options.option.optionValues.optionValue.value',
    'item.tagIds',
    'item.tagIds.tagId',
    'item.catchCopyForPC',
    'item.catchCopyForMobile',
    'item.descriptionBySalesMethod',
    'item.isSaleButton',
    'item.isDocumentButton',
    'item.isInquiryButton',
    'item.isStockNoticeButton',
    'item.itemLayout',
    'item.isIncludedTax',
    'item.isIncludedPostage',
    'item.isIncludedCashOnDeliveryPostage',
    'item.displayPrice',
    'item.orderLimit',
    'item.postage',
    'item.postageSegment1',
    'item.postageSegment2',
    'item.isNoshiEnable',
    'item.isTimeSale',
    'item.timeSaleStartDateTime',
    'item.timeSaleEndDateTime',
    'item.isUnavailableForSearch',
    'item.limitedPasswd',
    'item.isAvailableForMobile',
    'item.isDepot',
    'item.detailSellType',
    'item.releaseDate',
    'item.point',
    'item.point.pointRate',
    'item.point.pointRateStart',
    'item.point.pointRateEnd',
    'item.itemInventory',
    'item.itemInventory.inventoryType',
    'item.itemInventory.inventories',
    'item.itemInventory.inventories.inventory',
    'item.itemInventory.inventories.inventory.inventoryCount',
    'item.itemInventory.inventories.inventory.childNoVertical',
    'item.itemInventory.inventories.inventory.childNoHorizontal',
    'item.itemInventory.inventories.inventory.optionNameVertical',
    'item.itemInventory.inventories.inventory.optionNameHorizontal',
    'item.itemInventory.inventories.inventory.isBackorderAvailable',
    'item.itemInventory.inventories.inventory.normalDeliveryDateId',
    'item.itemInventory.inventories.inventory.backorderDeliveryDateId',
    'item.itemInventory.inventories.inventory.isBackorder',
    'item.itemInventory.inventories.inventory.isRestoreInventoryFlag',
    'item.itemInventory.inventories.inventory.images',
    'item.itemInventory.inventories.inventory.images.image',
    'item.itemInventory.inventories.inventory.images.image.imageUrl',
    'item.itemInventory.inventories.inventory.tagIds',
    'item.itemInventory.inventories.inventory.tagIds.tagId',
    'item.itemInventory.verticalName',
    'item.itemInventory.horizontalName',
    'item.itemInventory.inventoryQuantityFlag',
    'item.itemInventory.inventoryDisplayFlag',
    'item.asurakuDeliveryId',
    'item.sizeChartLinkCode',
    'item.reviewDisp',
    'item.medicine',
    'item.medicine.medCaption',
    'item.medicine.medAttention',
    'item.displayPriceId',
    'item.categories',
    'item.categories.categoryInfo',
    'item.categories.categoryInfo.categorySetManageNumber',
    'item.categories.categoryInfo.categoryId',
    'item.categories.categoryInfo.isPluralItemPage',
    'item.itemWeight',
    'item.layoutCommonId',
    'item.layoutMapId',
    'item.textSmallId',
    'item.lossLeaderId',
    'item.textLargeId',
]

item_update = [
    'item.itemUrl',
    'item.itemNumber',
    'item.itemName',
    'item.itemPrice',
    'item.genreId',
    'item.catalogId',
    'item.catalogIdExemptionReason',
    'item.images',
    'item.images.image',
    'item.images.image.imageUrl',
    'item.images.image.imageAlt',
    'item.descriptionForPC',
    'item.descriptionForMobile',
    'item.descriptionForSmartPhone',
    'item.movieUrl',
    'item.options',
    'item.options.option',
    'item.options.option.optionName',
    'item.options.option.optionStyle',
    'item.options.option.optionValues',
    'item.options.option.optionValues.optionValue',
    'item.options.option.optionValues.optionValue.value',
    'item.tagIds',
    'item.tagIds.tagId',
    'item.catchCopyForPC',
    'item.catchCopyForMobile',
    'item.descriptionBySalesMethod',
    'item.isSaleButton',
    'item.isDocumentButton',
    'item.isInquiryButton',
    'item.isStockNoticeButton',
    'item.itemLayout',
    'item.isIncludedTax',
    'item.isIncludedPostage',
    'item.isIncludedCashOnDeliveryPostage',
    'item.displayPrice',
    'item.orderLimit',
    'item.postage',
    'item.postageSegment1',
    'item.postageSegment2',
    'item.isNoshiEnable',
    'item.isTimeSale',
    'item.timeSaleStartDateTime',
    'item.timeSaleEndDateTime',
    'item.isUnavailableForSearch',
    'item.limitedPasswd',
    'item.isAvailableForMobile',
    'item.isDepot',
    'item.detailSellType',
    'item.releaseDate',
    'item.point',
    'item.point.pointRate',
    'item.point.pointRateStart',
    'item.point.pointRateEnd',
    'item.itemInventory',
    'item.itemInventory.inventoryType',
    'item.itemInventory.inventories',
    'item.itemInventory.inventories.inventory',
    'item.itemInventory.inventories.inventory.inventoryCount',
    'item.itemInventory.inventories.inventory.childNoVertical',
    'item.itemInventory.inventories.inventory.childNoHorizontal',
    'item.itemInventory.inventories.inventory.optionNameVertical',
    'item.itemInventory.inventories.inventory.optionNameHorizontal',
    'item.itemInventory.inventories.inventory.isBackorderAvailable',
    'item.itemInventory.inventories.inventory.normalDeliveryDateId',
    'item.itemInventory.inventories.inventory.backorderDeliveryDateId',
    'item.itemInventory.inventories.inventory.isBackorder',
    'item.itemInventory.inventories.inventory.isRestoreInventoryFlag',
    'item.itemInventory.inventories.inventory.images',
    'item.itemInventory.inventories.inventory.images.image',
    'item.itemInventory.inventories.inventory.images.image.imageUrl',
    'item.itemInventory.inventories.inventory.tagIds',
    'item.itemInventory.inventories.inventory.tagIds.tagId',
    'item.itemInventory.verticalName',
    'item.itemInventory.horizontalName',
    'item.itemInventory.inventoryQuantityFlag',
    'item.itemInventory.inventoryDisplayFlag',
    'item.asurakuDeliveryId',
    'item.sizeChartLinkCode',
    'item.reviewDisp',
    'item.medicine',
    'item.medicine.medCaption',
    'item.medicine.medAttention',
    'item.displayPriceId',
    'item.categories',
    'item.categories.categoryInfo',
    'item.categories.categoryInfo.categorySetManageNumber',
    'item.categories.categoryInfo.categoryId',
    'item.categories.categoryInfo.isPluralItemPage',
    'item.itemWeight',
    'item.layoutCommonId',
    'item.layoutMapId',
    'item.textSmallId',
    'item.lossLeaderId',
    'item.textLargeId',
]

item_delete = [
    'item.itemUrl'
]

items_update = [
    'items.item.itemUrl',
    'items.item.itemNumber',
    'items.item.itemName',
    'items.item.itemPrice',
    'items.item.genreId',
    'items.item.catalogId',
    'items.item.catalogIdExemptionReason',
    'items.item.catchCopyForPC',
    'items.item.catchCopyForMobile',
    'items.item.isIncludedTax',
    'items.item.isIncludedPostage',
    'items.item.displayPrice',
    'items.item.isUnavailableForSearch',
    'items.item.isAvailableForMobile',
    'items.item.isDepot',
    'items.item.categories',
    'items.item.categories.categoryInfo',
    'items.item.categories.categoryInfo.categorySetManageNumber',
    'items.item.categories.categoryInfo.categoryId',
    'items.item.categories.categoryInfo.isPluralItemPage',
    'items.item.itemWeight',
    'items.item.layoutCommonId',
    'items.item.layoutMapId',
    'items.item.textSmallId',
    'items.item.lossLeaderId',
    'items.item.textLargeId',
    'items.item.shopAreaSoryoPatternId',
    'items.item.taxRate',
]


cabinet_insert_file = [
    'file.fileName',
    'file.folderId',
    'file.filePath',
    'file.overWrite',
]


category_insert = [
    'categorySetManageNumber',
    'categoryId',
    'category.categoryId',
    'category.categoryLevel',
    'category.name',
    'category.status',
    'category.categoryWeight',
    'category.categoryContent.mainImageUrl',
    'category.categoryContent.mainImageAlt',
    'category.categoryContent.upperText',
    'category.categoryContent.lowerText',
    'category.categoryContent.smartPhoneText',
    'category.categoryLayout.layoutFrameworkId',
    'category.categoryLayout.layoutCategoryMapId',
    'category.categoryLayout.layoutTopTextId',
    'category.categoryLayout.layoutLossLeaderId',
    'category.categoryLayout.layoutCommonTextId',
    'category.categoryLayout.listingAreaId',
    'category.childCategories.category.categoryId',
    'category.childCategories.category.categoryLevel',
    'category.childCategories.category.name',
    'category.childCategories.category.status',
    'category.childCategories.category.categoryWeight',
    'category.childCategories.category.categoryContent',
    'category.childCategories.category.categoryContent.mainImageUrl',
    'category.childCategories.category.categoryContent.mainImageAlt',
    'category.childCategories.category.categoryContent.upperText',
    'category.childCategories.category.categoryContent.lowerText',
    'category.childCategories.category.categoryContent.smartPhoneText',
    'category.childCategories.category.categoryLayout',
    'category.childCategories.category.categoryLayout.layoutFrameworkId',
    'category.childCategories.category.categoryLayout.layoutCategoryMapId',
    'category.childCategories.category.categoryLayout.layoutTopTextId',
    'category.childCategories.category.categoryLayout.layoutLossLeaderId',
    'category.childCategories.category.categoryLayout.layoutCommonTextId',
    'category.childCategories.category.categoryLayout.listingAreaId',
    'category.childCategories.category.childCategories',
]


category_update = category_insert[1:]


category_move = [
    'categoryId',
    'categorySetManageNumber',
    'destCategoryId',
]
