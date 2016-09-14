#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 01 Jul 2016, 17:46:16
#========================================
import uuid, itertools
import maya.OpenMaya as OpenMaya
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
NODE_UUID_ATTR_NAME    = 'uuid'

DEFAULT_UUID           = '00000000000000000000000000000000'

MESSAGE_CALLBACK_ARRAY = OpenMaya.MCallbackIdArray()

#==================================================
# UUID Util ( Getting nodes and Informations )
#==================================================

def create_uuid():
    '''
    Create a string uuid hex code...
    '''
    uuid_code = uuid.uuid4()
    return uuid_code.get_hex()





def set_object_uuid(mobject, update=False, newID=None):
    '''
    Set a node's uuid attibute...
    '''
    MFn_node = OpenMaya.MFnDependencyNode(mobject)
    if MFn_node.isFromReferencedFile():
        return

    if MFn_node.isDefaultNode():
        return

    node_lock_status = MFn_node.isLocked()
    if node_lock_status:
        MFn_node.setLocked(False)

    uuid_plug = OpenMaya.MPlug()
    if MFn_node.hasAttribute(NODE_UUID_ATTR_NAME):
        if not update: #- do not change old uuid attribute
            return
        else: #- unlock old uuid attribute
            uuid_plug = MFn_node.findPlug(NODE_UUID_ATTR_NAME)
            uuid_plug.setLocked(False)

    else: #- add new uuid attribute
        MFn_attr = OpenMaya.MFnTypedAttribute()
        MOb_attr = MFn_attr.create(NODE_UUID_ATTR_NAME, NODE_UUID_ATTR_NAME, OpenMaya.MFnData.kString)

        MFn_node.addAttribute(MOb_attr)
        uuid_plug = MFn_node.findPlug(NODE_UUID_ATTR_NAME)

    #- set uuid attribute value...
    uuid_plug.setString(newID or create_uuid())
    uuid_plug.setLocked(True)

    MFn_node.setLocked(node_lock_status)





def get_scene_dependency_nodes(typ=OpenMaya.MFn.kInvalid, containReference=True):
    '''
    Get all of nodes in maya by input node type...
    '''
    iterator = OpenMaya.MItDependencyNodes(typ)
    while not iterator.isDone():
        if not containReference and OpenMaya.MFnDependencyNode(iterator.item()).isFromReferencedFile():
            iterator.next()
            continue
        yield iterator.item()
        iterator.next()





def get_scene_dag_parent_nodes(iterator):
    '''
    Get object's transform parents...
    '''
    for mobject in iterator:
        if mobject.hasFn(OpenMaya.MFn.kDagNode):
            MFn = OpenMaya.MFnDagNode(mobject)
            yield MFn.parent(0)





def get_scene_object_name(mobject):
    '''
    Get node's string name by maya api MObject...
    '''
    if mobject.hasFn(OpenMaya.MFn.kDagNode):
        MFn = OpenMaya.MFnDagNode(mobject)
        return MFn.fullPathName()
    else:
        MFn = OpenMaya.MFnDependencyNode(mobject)
        return MFn.name()





def get_uuid_by_object(mobject):
    '''
    Get node's uuid attrinbute value...
    '''
    dependency = OpenMaya.MFnDependencyNode(mobject)
    if dependency.hasAttribute(NODE_UUID_ATTR_NAME):
        return dependency.findPlug(NODE_UUID_ATTR_NAME).asString()
    else:
        return DEFAULT_UUID





def get_objects_by_uuid(uuid_code, typ=OpenMaya.MFn.kInvalid, containReference=True):
    '''
    Get nodes by input uuid hex...
    '''
    for mobject in get_scene_dependency_nodes(typ, containReference):
        if get_uuid_by_object(mobject) == uuid_code:
            yield mobject





#==================================================
# GET UUID ( Get uuid and nodes data )
#==================================================

def get_objects_uuid_data(iterator):
    '''
    Get objects uuid hex and node's MObject...
    '''
    for mobject in iterator:
        yield get_uuid_by_object(mobject), mobject





def get_scene_uuid_data(typ=OpenMaya.MFn.kInvalid, containReference=True):
    '''
    Get objects uuid hex and node's MObject by input node type...
    '''
    return get_objects_uuid_data(get_scene_dependency_nodes(typ, containReference))





def get_scene_transform_uuid_data(containReference=True):
    '''
    Get scene transform nodes uuid data...
    '''
    return get_scene_uuid_data(OpenMaya.MFn.kTransform, containReference)





def get_scene_camera_uuid_data(containReference=True):
    '''
    Get scene camera nodes uuid data...
    '''
    return itertools.chain(get_scene_uuid_data(OpenMaya.MFn.kCamera, containReference),
                           get_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kCamera, containReference))))





def get_scene_curve_uuid_data(containReference=True):
    '''
    Get scene curve nodes uuid data...
    '''
    return itertools.chain(get_scene_uuid_data(OpenMaya.MFn.kNurbsCurve, containReference),
                           get_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kNurbsCurve, containReference))))





def get_scene_nurbsSurface_uuid_data(containReference=True):
    '''
    Get scene nurbsSurfaces nodes uuid data...
    '''
    return itertools.chain(get_scene_uuid_data(OpenMaya.MFn.kNurbsSurface, containReference),
                           get_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kNurbsSurface, containReference))))





def get_scene_polygon_uuid_data(containReference=True):
    '''
    Get scene polygon nodes uuid data...
    '''
    return itertools.chain(get_scene_uuid_data(OpenMaya.MFn.kMesh, containReference),
                           get_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kMesh, containReference))))





def get_scene_subdiv_uuid_data(containReference=True):
    '''
    Get scene subdiv nodes uuid data...
    '''
    return itertools.chain(get_scene_uuid_data(OpenMaya.MFn.kSubdiv, containReference),
                           get_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kSubdiv, containReference))))





def get_scene_geometry_uuid_data(containReference=True):
    '''
    Get scene nurbsSurface polygon and subdiv nodes uuid data...
    '''
    return itertools.chain(get_scene_nurbsSurface_uuid_data(containReference),
                           get_scene_polygon_uuid_data(containReference),
                           get_scene_subdiv_uuid_data(containReference))





def get_scene_shadingEngine_uuid_data(containReference=True):
    '''
    Get scene shadingEngine nodes uuid data...
    '''
    return get_scene_uuid_data(OpenMaya.MFn.kShadingEngine, containReference)





def get_scene_joint_uuid_data(containReference=True):
    '''
    Get scene joint nodes uuid data...
    '''
    return get_scene_uuid_data(OpenMaya.MFn.kJoint, containReference)





def get_scene_selection_uuid_data(selection):
    '''
    Get scene selection nodes uuid data...
    '''
    iterator = OpenMaya.MItSelectionList(selection)
    while not iterator.isDone():
        mobject = OpenMaya.MObject()
        iterator.getDependNode(mobject)

        yield get_uuid_by_object(mobject), mobject

        iterator.next()





#==================================================
# SET UUID ( Add uuid for nodes )
#==================================================

def set_objects_uuid_data(iterator, update=False):
    '''
    Set objects uuid attribute...
    '''
    for mobject in iterator:
        set_object_uuid(mobject, update)





def set_scene_uuid_data(typ=OpenMaya.MFn.kInvalid, update=False):
    '''
    Set objects uuid attribute by input node type...
    '''
    set_objects_uuid_data(get_scene_dependency_nodes(typ, False), update)





def set_scene_transform_uuid_data(update=False):
    '''
    Set transform object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kTransform, update)





def set_scene_camera_uuid_data(update=False):
    '''
    Set camera object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kCamera, update)
    set_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kCamera, False)))





def set_scene_curve_uuid_data(update=False):
    '''
    Set curve object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kNurbsCurve, update)
    set_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kNurbsCurve, False)))





def set_scene_nurbsSurface_uuid_data(update=False):
    '''
    Set nurbsSurface object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kNurbsSurface, update)
    set_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kNurbsSurface, False)))





def set_scene_polygon_uuid_data(update=False):
    '''
    Set polygon object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kMesh, update)
    set_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kMesh, False)))





def set_scene_subdiv_uuid_data(update=False):
    '''
    Set subdiv object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kSubdiv, update)
    set_objects_uuid_data(get_scene_dag_parent_nodes(get_scene_dependency_nodes(OpenMaya.MFn.kSubdiv, False)))





def set_scene_geometry_uuid_data(update=False):
    '''
    Set nurbsSurface polygon and subdiv object's uuid attribute...
    '''
    set_scene_nurbsSurface_uuid_data(update)
    set_scene_polygon_uuid_data(update)
    set_scene_subdiv_uuid_data(update)





def set_scene_shadingEngine_uuid_data(update=False):
    '''
    Set shadingEngine object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kShadingEngine, update)





def set_scene_joint_uuid_data(update=False):
    '''
    Set joint object's uuid attribute...
    '''
    set_scene_uuid_data(OpenMaya.MFn.kJoint, update)





def set_scene_selection_uuid_data(selection, update=False):
    '''
    Set selection object's uuid attribute...
    '''
    iterator = OpenMaya.MItSelectionList(selection)
    while not iterator.isDone():
        mobject = OpenMaya.MObject()
        iterator.getDependNode(mobject)

        set_object_uuid(mobject, update)

        iterator.next()





def set_scene_duplicates_uuid_to_new(typ=OpenMaya.MFn.kInvalid):
    '''
    '''
    uuid_list = [DEFAULT_UUID]
    for node_uuid, mobject in get_scene_uuid_data(typ):
        if node_uuid in uuid_list:
            set_object_uuid(mobject, True)
        uuid_list.append(node_uuid)





#==================================================
# SCENE MESSAGE ( Event for add uuid )
#==================================================

def node_add_message_callback(*args):
    '''
    add uuid to node when node created...
    '''
    if OpenMaya.MFileIO.isReadingFile() or OpenMaya.MFileIO.isOpeningFile():
        return
    set_object_uuid(args[0])





def file_read_message_callback(*args):
    '''
    add uuid to node when file imported...
    '''
    set_scene_uuid_data()





def add_scene_message_callback():
    '''
    Create a message track to call message callback...
    '''
    if MESSAGE_CALLBACK_ARRAY.length() > 0:
        return
    #-
    MESSAGE_CALLBACK_ARRAY.append(OpenMaya.MDGMessage.addNodeAddedCallback(node_add_message_callback))
    #-
    MESSAGE_CALLBACK_ARRAY.append(OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterFileRead, file_read_message_callback))





def remove_scene_message_callback():
    '''
    Remove scene message callbacks...
    '''
    OpenMaya.MMessage.removeCallbacks(MESSAGE_CALLBACK_ARRAY)
    MESSAGE_CALLBACK_ARRAY.clear()
