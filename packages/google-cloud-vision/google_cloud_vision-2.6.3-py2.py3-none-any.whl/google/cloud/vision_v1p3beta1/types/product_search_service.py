# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore

from google.cloud.vision_v1p3beta1.types import geometry
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.vision.v1p3beta1",
    manifest={
        "Product",
        "ProductSet",
        "ReferenceImage",
        "CreateProductRequest",
        "ListProductsRequest",
        "ListProductsResponse",
        "GetProductRequest",
        "UpdateProductRequest",
        "DeleteProductRequest",
        "CreateProductSetRequest",
        "ListProductSetsRequest",
        "ListProductSetsResponse",
        "GetProductSetRequest",
        "UpdateProductSetRequest",
        "DeleteProductSetRequest",
        "CreateReferenceImageRequest",
        "ListReferenceImagesRequest",
        "ListReferenceImagesResponse",
        "GetReferenceImageRequest",
        "DeleteReferenceImageRequest",
        "AddProductToProductSetRequest",
        "RemoveProductFromProductSetRequest",
        "ListProductsInProductSetRequest",
        "ListProductsInProductSetResponse",
        "ImportProductSetsGcsSource",
        "ImportProductSetsInputConfig",
        "ImportProductSetsRequest",
        "ImportProductSetsResponse",
        "BatchOperationMetadata",
    },
)


class Product(proto.Message):
    r"""A Product contains ReferenceImages.

    Attributes:
        name (str):
            The resource name of the product.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``.

            This field is ignored when creating a product.
        display_name (str):
            The user-provided name for this Product. Must
            not be empty. Must be at most 4096 characters
            long.
        description (str):
            User-provided metadata to be stored with this
            product. Must be at most 4096 characters long.
        product_category (str):
            Immutable. The category for the product
            identified by the reference image. This should
            be either "homegoods-v2", "apparel-v2", or
            "toys-v2". The legacy categories "homegoods",
            "apparel", and "toys" are still supported, but
            these should not be used for new products.
        product_labels (Sequence[google.cloud.vision_v1p3beta1.types.Product.KeyValue]):
            Key-value pairs that can be attached to a product. At query
            time, constraints can be specified based on the
            product_labels.

            Note that integer values can be provided as strings, e.g.
            "1199". Only strings with integer values can match a
            range-based restriction which is to be supported soon.

            Multiple values can be assigned to the same key. One product
            may have up to 100 product_labels.
    """

    class KeyValue(proto.Message):
        r"""A product label represented as a key-value pair.

        Attributes:
            key (str):
                The key of the label attached to the product.
                Cannot be empty and cannot exceed 128 bytes.
            value (str):
                The value of the label attached to the
                product. Cannot be empty and cannot exceed 128
                bytes.
        """

        key = proto.Field(proto.STRING, number=1,)
        value = proto.Field(proto.STRING, number=2,)

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    product_category = proto.Field(proto.STRING, number=4,)
    product_labels = proto.RepeatedField(proto.MESSAGE, number=5, message=KeyValue,)


class ProductSet(proto.Message):
    r"""A ProductSet contains Products. A ProductSet can contain a
    maximum of 1 million reference images. If the limit is exceeded,
    periodic indexing will fail.

    Attributes:
        name (str):
            The resource name of the ProductSet.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``.

            This field is ignored when creating a ProductSet.
        display_name (str):
            The user-provided name for this ProductSet.
            Must not be empty. Must be at most 4096
            characters long.
        index_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            ProductSet was last indexed. Query results will
            reflect all updates before this time. If this
            ProductSet has never been indexed, this field is
            0.

            This field is ignored when creating a
            ProductSet.
        index_error (google.rpc.status_pb2.Status):
            Output only. If there was an error with
            indexing the product set, the field is
            populated.
            This field is ignored when creating a
            ProductSet.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    index_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    index_error = proto.Field(proto.MESSAGE, number=4, message=status_pb2.Status,)


class ReferenceImage(proto.Message):
    r"""A ``ReferenceImage`` represents a product image and its associated
    metadata, such as bounding boxes.

    Attributes:
        name (str):
            The resource name of the reference image.

            Format is:

            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID/referenceImages/IMAGE_ID``.

            This field is ignored when creating a reference image.
        uri (str):
            Required. The Google Cloud Storage URI of the reference
            image.

            The URI must start with ``gs://``.
        bounding_polys (Sequence[google.cloud.vision_v1p3beta1.types.BoundingPoly]):
            Optional. Bounding polygons around the areas
            of interest in the reference image. If this
            field is empty, the system will try to detect
            regions of interest. At most 10 bounding
            polygons will be used.
            The provided shape is converted into a non-
            rotated rectangle. Once converted, the small
            edge of the rectangle must be greater than or
            equal to 300 pixels. The aspect ratio must be
            1:4 or less (i.e. 1:3 is ok; 1:5 is not).
    """

    name = proto.Field(proto.STRING, number=1,)
    uri = proto.Field(proto.STRING, number=2,)
    bounding_polys = proto.RepeatedField(
        proto.MESSAGE, number=3, message=geometry.BoundingPoly,
    )


class CreateProductRequest(proto.Message):
    r"""Request message for the ``CreateProduct`` method.

    Attributes:
        parent (str):
            Required. The project in which the Product should be
            created.

            Format is ``projects/PROJECT_ID/locations/LOC_ID``.
        product (google.cloud.vision_v1p3beta1.types.Product):
            Required. The product to create.
        product_id (str):
            A user-supplied resource id for this Product. If set, the
            server will attempt to use this value as the resource id. If
            it is already in use, an error is returned with code
            ALREADY_EXISTS. Must be at most 128 characters long. It
            cannot contain the character ``/``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    product = proto.Field(proto.MESSAGE, number=2, message="Product",)
    product_id = proto.Field(proto.STRING, number=3,)


class ListProductsRequest(proto.Message):
    r"""Request message for the ``ListProducts`` method.

    Attributes:
        parent (str):
            Required. The project OR ProductSet from which Products
            should be listed.

            Format: ``projects/PROJECT_ID/locations/LOC_ID``
        page_size (int):
            The maximum number of items to return.
            Default 10, maximum 100.
        page_token (str):
            The next_page_token returned from a previous List request,
            if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListProductsResponse(proto.Message):
    r"""Response message for the ``ListProducts`` method.

    Attributes:
        products (Sequence[google.cloud.vision_v1p3beta1.types.Product]):
            List of products.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    products = proto.RepeatedField(proto.MESSAGE, number=1, message="Product",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetProductRequest(proto.Message):
    r"""Request message for the ``GetProduct`` method.

    Attributes:
        name (str):
            Required. Resource name of the Product to get.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateProductRequest(proto.Message):
    r"""Request message for the ``UpdateProduct`` method.

    Attributes:
        product (google.cloud.vision_v1p3beta1.types.Product):
            Required. The Product resource which replaces
            the one on the server. product.name is
            immutable.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The [FieldMask][google.protobuf.FieldMask] that specifies
            which fields to update. If update_mask isn't specified, all
            mutable fields are to be updated. Valid mask paths include
            ``product_labels``, ``display_name``, and ``description``.
    """

    product = proto.Field(proto.MESSAGE, number=1, message="Product",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteProductRequest(proto.Message):
    r"""Request message for the ``DeleteProduct`` method.

    Attributes:
        name (str):
            Required. Resource name of product to delete.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateProductSetRequest(proto.Message):
    r"""Request message for the ``CreateProductSet`` method.

    Attributes:
        parent (str):
            Required. The project in which the ProductSet should be
            created.

            Format is ``projects/PROJECT_ID/locations/LOC_ID``.
        product_set (google.cloud.vision_v1p3beta1.types.ProductSet):
            Required. The ProductSet to create.
        product_set_id (str):
            A user-supplied resource id for this ProductSet. If set, the
            server will attempt to use this value as the resource id. If
            it is already in use, an error is returned with code
            ALREADY_EXISTS. Must be at most 128 characters long. It
            cannot contain the character ``/``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    product_set = proto.Field(proto.MESSAGE, number=2, message="ProductSet",)
    product_set_id = proto.Field(proto.STRING, number=3,)


class ListProductSetsRequest(proto.Message):
    r"""Request message for the ``ListProductSets`` method.

    Attributes:
        parent (str):
            Required. The project from which ProductSets should be
            listed.

            Format is ``projects/PROJECT_ID/locations/LOC_ID``.
        page_size (int):
            The maximum number of items to return.
            Default 10, maximum 100.
        page_token (str):
            The next_page_token returned from a previous List request,
            if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListProductSetsResponse(proto.Message):
    r"""Response message for the ``ListProductSets`` method.

    Attributes:
        product_sets (Sequence[google.cloud.vision_v1p3beta1.types.ProductSet]):
            List of ProductSets.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    product_sets = proto.RepeatedField(proto.MESSAGE, number=1, message="ProductSet",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetProductSetRequest(proto.Message):
    r"""Request message for the ``GetProductSet`` method.

    Attributes:
        name (str):
            Required. Resource name of the ProductSet to get.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateProductSetRequest(proto.Message):
    r"""Request message for the ``UpdateProductSet`` method.

    Attributes:
        product_set (google.cloud.vision_v1p3beta1.types.ProductSet):
            Required. The ProductSet resource which
            replaces the one on the server.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The [FieldMask][google.protobuf.FieldMask] that specifies
            which fields to update. If update_mask isn't specified, all
            mutable fields are to be updated. Valid mask path is
            ``display_name``.
    """

    product_set = proto.Field(proto.MESSAGE, number=1, message="ProductSet",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteProductSetRequest(proto.Message):
    r"""Request message for the ``DeleteProductSet`` method.

    Attributes:
        name (str):
            Required. Resource name of the ProductSet to delete.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateReferenceImageRequest(proto.Message):
    r"""Request message for the ``CreateReferenceImage`` method.

    Attributes:
        parent (str):
            Required. Resource name of the product in which to create
            the reference image.

            Format is
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``.
        reference_image (google.cloud.vision_v1p3beta1.types.ReferenceImage):
            Required. The reference image to create.
            If an image ID is specified, it is ignored.
        reference_image_id (str):
            A user-supplied resource id for the ReferenceImage to be
            added. If set, the server will attempt to use this value as
            the resource id. If it is already in use, an error is
            returned with code ALREADY_EXISTS. Must be at most 128
            characters long. It cannot contain the character ``/``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    reference_image = proto.Field(proto.MESSAGE, number=2, message="ReferenceImage",)
    reference_image_id = proto.Field(proto.STRING, number=3,)


class ListReferenceImagesRequest(proto.Message):
    r"""Request message for the ``ListReferenceImages`` method.

    Attributes:
        parent (str):
            Required. Resource name of the product containing the
            reference images.

            Format is
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``.
        page_size (int):
            The maximum number of items to return.
            Default 10, maximum 100.
        page_token (str):
            A token identifying a page of results to be returned. This
            is the value of ``nextPageToken`` returned in a previous
            reference image list request.

            Defaults to the first page if not specified.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListReferenceImagesResponse(proto.Message):
    r"""Response message for the ``ListReferenceImages`` method.

    Attributes:
        reference_images (Sequence[google.cloud.vision_v1p3beta1.types.ReferenceImage]):
            The list of reference images.
        page_size (int):
            The maximum number of items to return.
            Default 10, maximum 100.
        next_page_token (str):
            The next_page_token returned from a previous List request,
            if any.
    """

    @property
    def raw_page(self):
        return self

    reference_images = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ReferenceImage",
    )
    page_size = proto.Field(proto.INT32, number=2,)
    next_page_token = proto.Field(proto.STRING, number=3,)


class GetReferenceImageRequest(proto.Message):
    r"""Request message for the ``GetReferenceImage`` method.

    Attributes:
        name (str):
            Required. The resource name of the ReferenceImage to get.

            Format is:

            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID/referenceImages/IMAGE_ID``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteReferenceImageRequest(proto.Message):
    r"""Request message for the ``DeleteReferenceImage`` method.

    Attributes:
        name (str):
            Required. The resource name of the reference image to
            delete.

            Format is:

            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID/referenceImages/IMAGE_ID``
    """

    name = proto.Field(proto.STRING, number=1,)


class AddProductToProductSetRequest(proto.Message):
    r"""Request message for the ``AddProductToProductSet`` method.

    Attributes:
        name (str):
            Required. The resource name for the ProductSet to modify.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
        product (str):
            Required. The resource name for the Product to be added to
            this ProductSet.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
    """

    name = proto.Field(proto.STRING, number=1,)
    product = proto.Field(proto.STRING, number=2,)


class RemoveProductFromProductSetRequest(proto.Message):
    r"""Request message for the ``RemoveProductFromProductSet`` method.

    Attributes:
        name (str):
            Required. The resource name for the ProductSet to modify.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
        product (str):
            Required. The resource name for the Product to be removed
            from this ProductSet.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
    """

    name = proto.Field(proto.STRING, number=1,)
    product = proto.Field(proto.STRING, number=2,)


class ListProductsInProductSetRequest(proto.Message):
    r"""Request message for the ``ListProductsInProductSet`` method.

    Attributes:
        name (str):
            Required. The ProductSet resource for which to retrieve
            Products.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
        page_size (int):
            The maximum number of items to return.
            Default 10, maximum 100.
        page_token (str):
            The next_page_token returned from a previous List request,
            if any.
    """

    name = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListProductsInProductSetResponse(proto.Message):
    r"""Response message for the ``ListProductsInProductSet`` method.

    Attributes:
        products (Sequence[google.cloud.vision_v1p3beta1.types.Product]):
            The list of Products.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    products = proto.RepeatedField(proto.MESSAGE, number=1, message="Product",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class ImportProductSetsGcsSource(proto.Message):
    r"""The Google Cloud Storage location for a csv file which
    preserves a list of ImportProductSetRequests in each line.

    Attributes:
        csv_file_uri (str):
            The Google Cloud Storage URI of the input csv file.

            The URI must start with ``gs://``.

            The format of the input csv file should be one image per
            line. In each line, there are 6 columns.

            1. image_uri 2, image_id
            2. product_set_id
            3. product_id 5, product_category 6, product_display_name 7,
               labels
            4. bounding_poly

            Columns 1, 3, 4, and 5 are required, other columns are
            optional. A new ProductSet/Product with the same id will be
            created on the fly if the ProductSet/Product specified by
            product_set_id/product_id does not exist.

            The image_id field is optional but has to be unique if
            provided. If it is empty, we will automatically assign an
            unique id to the image.

            The product_display_name field is optional. If it is empty,
            a space (" ") is used as the place holder for the product
            display_name, which can be updated later through the
            realtime API.

            If the Product with product_id already exists, the fields
            product_display_name, product_category and labels are
            ignored.

            If a Product doesn't exist and needs to be created on the
            fly, the product_display_name field refers to
            [Product.display_name][google.cloud.vision.v1p3beta1.Product.display_name],
            the product_category field refers to
            [Product.product_category][google.cloud.vision.v1p3beta1.Product.product_category],
            and the labels field refers to [Product.labels][].

            Labels (optional) should be a line containing a list of
            comma-separated key-value pairs, with the format
            "key_1=value_1,key_2=value_2,...,key_n=value_n".

            The bounding_poly (optional) field is used to identify one
            region of interest from the image in the same manner as
            CreateReferenceImage. If no bounding_poly is specified, the
            system will try to detect regions of interest automatically.

            Note that the pipeline will resize the image if the image
            resolution is too large to process (above 20MP).

            Also note that at most one bounding_poly is allowed per
            line. If the image contains multiple regions of interest,
            the csv should contain one line per region of interest.

            The bounding_poly column should contain an even number of
            comma-separated numbers, with the format
            "p1_x,p1_y,p2_x,p2_y,...,pn_x,pn_y". Nonnegative integers
            should be used for absolute bounding polygons, and float
            values in [0, 1] should be used for normalized bounding
            polygons.
    """

    csv_file_uri = proto.Field(proto.STRING, number=1,)


class ImportProductSetsInputConfig(proto.Message):
    r"""The input content for the ``ImportProductSets`` method.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_source (google.cloud.vision_v1p3beta1.types.ImportProductSetsGcsSource):
            The Google Cloud Storage location for a csv
            file which preserves a list of
            ImportProductSetRequests in each line.

            This field is a member of `oneof`_ ``source``.
    """

    gcs_source = proto.Field(
        proto.MESSAGE, number=1, oneof="source", message="ImportProductSetsGcsSource",
    )


class ImportProductSetsRequest(proto.Message):
    r"""Request message for the ``ImportProductSets`` method.

    Attributes:
        parent (str):
            Required. The project in which the ProductSets should be
            imported.

            Format is ``projects/PROJECT_ID/locations/LOC_ID``.
        input_config (google.cloud.vision_v1p3beta1.types.ImportProductSetsInputConfig):
            Required. The input content for the list of
            requests.
    """

    parent = proto.Field(proto.STRING, number=1,)
    input_config = proto.Field(
        proto.MESSAGE, number=2, message="ImportProductSetsInputConfig",
    )


class ImportProductSetsResponse(proto.Message):
    r"""Response message for the ``ImportProductSets`` method.

    This message is returned by the
    [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
    method in the returned
    [google.longrunning.Operation.response][google.longrunning.Operation.response]
    field.

    Attributes:
        reference_images (Sequence[google.cloud.vision_v1p3beta1.types.ReferenceImage]):
            The list of reference_images that are imported successfully.
        statuses (Sequence[google.rpc.status_pb2.Status]):
            The rpc status for each ImportProductSet request, including
            both successes and errors.

            The number of statuses here matches the number of lines in
            the csv file, and statuses[i] stores the success or failure
            status of processing the i-th line of the csv, starting from
            line 0.
    """

    reference_images = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ReferenceImage",
    )
    statuses = proto.RepeatedField(proto.MESSAGE, number=2, message=status_pb2.Status,)


class BatchOperationMetadata(proto.Message):
    r"""Metadata for the batch operations such as the current state.

    This is included in the ``metadata`` field of the ``Operation``
    returned by the ``GetOperation`` call of the
    ``google::longrunning::Operations`` service.

    Attributes:
        state (google.cloud.vision_v1p3beta1.types.BatchOperationMetadata.State):
            The current state of the batch operation.
        submit_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the batch request was submitted
            to the server.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the batch request is finished and
            [google.longrunning.Operation.done][google.longrunning.Operation.done]
            is set to true.
    """

    class State(proto.Enum):
        r"""Enumerates the possible states that the batch request can be
        in.
        """
        STATE_UNSPECIFIED = 0
        PROCESSING = 1
        SUCCESSFUL = 2
        FAILED = 3
        CANCELLED = 4

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    submit_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
