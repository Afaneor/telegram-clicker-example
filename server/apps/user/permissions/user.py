import rules
from rules.predicates import is_authenticated

rules.set_perm('user.view_user', is_authenticated)
rules.set_perm('user.change_user', is_authenticated)
rules.set_perm('user.list_user', is_authenticated)
rules.set_perm('user.action_is_authenticated_user', is_authenticated)
