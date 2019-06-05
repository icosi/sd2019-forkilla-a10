from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class Comercial_permission(permissions.BasePermission):
   
    def has_permission(self,request,view):
        #permiso de lectura HEAD,GET..
        if request.method in permissions.SAFE_METHODS:
            return True
        #comerciales
        return request.user.groups.filter(name='Comerciales').exists()


       
   
class read_run_permission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
    
        return request.user.groups.filter(name='Comerciales').exists()