from django.conf import settings

from isc_common import dictinct_list
from isc_common.common.mat_views import refresh_mat_view
from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException, JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.operation_locations_view import Operation_locations_view, Operation_locations_viewManager
from kaf_pas.planing.models.operation_resources_view import Operation_resources_view
from kaf_pas.planing.models.production_order import Production_order, Production_orderManager
from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch, Production_order_per_launchManager


@JsonResponseWithException()
def Production_order_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)

    data = _request.get_data()
    arranged = data.get('arranged')
    location_id = data.get('location_id')

    if arranged == None:
        arranged = False

    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'item').
                    filter(opertype__in=opers_types).
                    filter(location_ids__overlap=[location_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ) if arranged == False else Production_order.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'item').
                    filter(opertype__in=opers_types).
                    filter(arranges_exucutors__isnull=False).
                    filter(location_ids__overlap=[location_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'item').
                    filter(opertype__in=opers_types).
                    filter(exucutors__overlap=[_request.user_id]).
                    filter(location_ids__overlap=[location_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ) if arranged == False else Production_order.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'item').
                    filter(opertype__in=opers_types).
                    filter(arranges_exucutors__overlap=[_request.user_id]).
                    filter(location_ids__overlap=[location_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_per_launch_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    # print(_request.json.get('data'))
    data = _request.get_data()
    location_id = data.get('location_id')

    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_per_launch.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'item').
                    filter(opertype__in=opers_types).
                    filter(location_ids__overlap=[location_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_per_launch.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'item').
                    filter(opertype__in=opers_types).
                    filter(exucutors__overlap=[_request.user_id]).
                    filter(location_ids__overlap=[location_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLocations(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)

    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_locations_view.objects.
                    filter(
                    opertype__in=opers_types,
                    props__in=[Production_order.props.product_order_routing]
                ).
                    distinct().
                    order_by('location__name').
                    get_range_rows1(
                    request=request,
                    function=Operation_locations_viewManager.getRecordLocations
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_locations_view.objects.
                    filter(executor__in=[_request.user_id]).
                    filter(
                    opertype__in=opers_types,
                    props__in=[Production_order.props.product_order_routing]
                ).
                    distinct().
                    order_by('location__name').
                    get_range_rows1(
                    request=request,
                    function=Operation_locations_viewManager.getRecordLocations,
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLevels(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing,
                    ]
                ).
                    order_by('level__code').
                    values('level_id', 'level__name', 'level__code').
                    distinct().
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLevels
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(executor__in=[_request.user_id]).
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing,
                    ]
                ).
                    order_by('level__code').
                    values('level_id', 'level__name', 'level__code').
                    distinct().
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLevels
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchExecutorsLocation(request):
    from kaf_pas.ckk.models.locations_users import Locations_users
    from kaf_pas.ckk.models.locations_users import Locations_usersManager
    return JsonResponse(
        DSResponse(
            request=request,
            data=Locations_users.objects.
                filter().
                distinct().
                get_range_rows1(
                request=request,
                function=Locations_usersManager.getRecord1),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_UpdateForwarding(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequestUpdateForwarding(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_SetStartStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_setStartStatus(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_getValue_made(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getValue_made(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def User_Fetch4(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getLoocationUsers(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_MakeProdOrder(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.makeProdOrderFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_DeleteProdOrder(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.deleteProdOrderFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_RefreshRows(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.refreshRowsProdOrderFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_RefreshMView(request):
    refresh_mat_view('planing_production_order_mview')
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)
