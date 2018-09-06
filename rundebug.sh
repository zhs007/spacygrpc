docker run \
    -p 3733:3733 \
    --name spacygrpc \
    -v $PWD/src:/home/spacygrpc \
    spacygrpc