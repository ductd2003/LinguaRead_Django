from myapp.views import refresh_levels_and_languages_cache

# Hàm tự động làm mới cache
def refresh_cache_task():
    refresh_levels_and_languages_cache()
    print("Cache for levels and languages has been refreshed.")
