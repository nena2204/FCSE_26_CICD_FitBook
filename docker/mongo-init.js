const replicaSetName = process.env.MONGO_REPLICA_SET || "rs0";
const databaseName = process.env.MONGO_DB_NAME || "fitbook_db";
const applicationUser = process.env.MONGO_APP_USERNAME;
const applicationPassword = process.env.MONGO_APP_PASSWORD;

let replicaSetInitialized = false;

try {
    const currentStatus = rs.status();

    if (currentStatus.ok === 1) {
        replicaSetInitialized = true;
        print("Replica set is already initialized.");
    }
} catch (error) {
    if (error.code !== 94 && error.codeName !== "NotYetInitialized") {
        throw error;
    }
}

if (!replicaSetInitialized) {
    print("Initializing MongoDB replica set...");

    const result = rs.initiate({
        _id: replicaSetName,
        members: [
            {
                _id: 0,
                host: "mongo1:27017",
                priority: 2
            },
            {
                _id: 1,
                host: "mongo2:27017",
                priority: 1
            },
            {
                _id: 2,
                host: "mongo3:27017",
                priority: 1
            }
        ]
    });

    printjson(result);
}

let primaryReady = false;

for (let attempt = 1; attempt <= 60; attempt++) {
    try {
        const helloResult = db.adminCommand({ hello: 1 });

        if (helloResult.isWritablePrimary) {
            primaryReady = true;
            print("MongoDB Primary is ready.");
            break;
        }
    } catch (error) {
        print(`Waiting for Primary, attempt ${attempt}/60...`);
    }

    sleep(1000);
}

if (!primaryReady) {
    throw new Error("MongoDB Primary was not elected in time.");
}

if (!applicationUser || !applicationPassword) {
    throw new Error(
        "MONGO_APP_USERNAME and MONGO_APP_PASSWORD must be configured."
    );
}

const applicationDatabase = db.getSiblingDB(databaseName);
const existingUser = applicationDatabase.getUser(applicationUser);

if (existingUser === null) {
    applicationDatabase.createUser({
        user: applicationUser,
        pwd: applicationPassword,
        roles: [
            {
                role: "readWrite",
                db: databaseName
            }
        ]
    });

    print(`Created application user for database: ${databaseName}`);
} else {
    print("Application database user already exists.");
}

print("MongoDB replica-set initialization completed.");