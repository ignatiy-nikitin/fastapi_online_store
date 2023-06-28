import datetime
from datetime import UTC

from factory import fuzzy, Sequence, SubFactory, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText

from auth import models as auth_models
from auth import utils as auth_utils
from carts import models as carts_models
from orders import models as orders_models
from products import models as products_models
from .databases import Session


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class ProductFactory(BaseFactory):
    title = FuzzyText()
    description = FuzzyText()
    price = fuzzy.FuzzyDecimal(low=1, high=10000)

    class Meta:
        model = products_models.Product

    @post_generation
    def images(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for image in extracted:
                self.images.append(image)
        else:
            for _ in range(5):
                ProductImageFactory.create(product=self)


class ProductImageFactory(BaseFactory):
    path = FuzzyText()
    product = SubFactory(ProductFactory)

    class Meta:
        model = products_models.ProductImage


class UserFactory(BaseFactory):
    email = Sequence(lambda n: f"user{n}@example.com")
    username = fuzzy.FuzzyText()
    password = auth_utils.get_password_hash('password')
    name = FuzzyText()
    age = fuzzy.FuzzyInteger(low=1, high=100)
    role = fuzzy.FuzzyChoice([e.value for e in auth_models.UserRoles])

    class Meta:
        model = auth_models.User

    @post_generation
    def cart(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.cart_id = extracted.id


class UserClientFactory(UserFactory):
    role = auth_models.UserRoles.client


class UserOperatorFactory(UserFactory):
    role = auth_models.UserRoles.operator


class UserAdminFactory(UserFactory):
    role = auth_models.UserRoles.admin


class CartFactory(BaseFactory):
    user = SubFactory(UserClientFactory)

    class Meta:
        model = carts_models.Cart

    @post_generation
    def cart_items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cart_item in extracted:
                self.cart_items.append(cart_item)


class CartItemFactory(BaseFactory):
    quantity = fuzzy.FuzzyInteger(low=1, high=100)
    price = fuzzy.FuzzyInteger(low=100, high=1000)
    cart = SubFactory(CartFactory)
    product = SubFactory(ProductFactory)

    class Meta:
        model = carts_models.CartItem


class OrderFactory(BaseFactory):
    created_dt = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2008, 1, 1, tzinfo=UTC))
    delivery_dt = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2008, 1, 1, tzinfo=UTC))
    address = fuzzy.FuzzyText()
    total_cost = fuzzy.FuzzyDecimal(low=100)
    status = orders_models.OrderStatus.created
    user = SubFactory(UserClientFactory)
    cart = SubFactory(CartFactory)

    class Meta:
        model = orders_models.Order

    @post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.user_id = extracted.id

    @post_generation
    def cart(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.cart_id = extracted.id
