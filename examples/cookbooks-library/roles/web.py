name = "web-role-name"
description = "Role description"
run_list = 'recipe.nginx', 'recipe.postgres.recipename'
depends_on = 'sudo', 'sysctl'
