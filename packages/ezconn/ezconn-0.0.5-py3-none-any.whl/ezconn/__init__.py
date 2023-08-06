import os
import jaydebeapi
   
def connect(db_type, host, port, database, username, password, ssl=False, driver_dir="/var/jdbc"):
    db_properties = {}

    # Vertica settings
    db_properties["vertica"] = {}
    db_properties["vertica"]["driver_class"] = "com.vertica.jdbc.Driver"
    db_properties["vertica"]["connection_string_template"] = "jdbc:vertica://{host}:{port}/{database}"

    # ClickHouse settings
    db_properties["clickhouse"] = {}
    db_properties["clickhouse"]["driver_class"] = "ru.yandex.clickhouse.ClickHouseDriver"
    db_properties["clickhouse"]["connection_string_template"] = "jdbc:clickhouse://{host}:{port}/{database}"
    if db_type == "clickhouse" and ssl:
        db_properties["clickhouse"]["connection_string_template"] += "?ssl=true&sslmode=strict"

    driver_class = db_properties[db_type]["driver_class"]
    
    conn_str = db_properties[db_type]["connection_string_template"].format(
                    host=host, port=port, database=database)
    
    driver_path = os.path.join(driver_dir, db_type + "-jdbc.jar")
    
    
    return jaydebeapi.connect(driver_class, conn_str, [username, password], driver_path)