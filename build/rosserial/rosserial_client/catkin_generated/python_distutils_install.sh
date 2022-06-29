#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/pi/Documents/ros_tracker/src/rosserial/rosserial_client"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/pi/Documents/ros_tracker/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/pi/Documents/ros_tracker/install/lib/python2.7/dist-packages:/home/pi/Documents/ros_tracker/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/pi/Documents/ros_tracker/build" \
    "/usr/bin/python2" \
    "/home/pi/Documents/ros_tracker/src/rosserial/rosserial_client/setup.py" \
     \
    build --build-base "/home/pi/Documents/ros_tracker/build/rosserial/rosserial_client" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/pi/Documents/ros_tracker/install" --install-scripts="/home/pi/Documents/ros_tracker/install/bin"
