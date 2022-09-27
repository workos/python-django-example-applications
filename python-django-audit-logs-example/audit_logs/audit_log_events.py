from datetime import datetime

user_signed_in = {
    "action": "user.signed_in",
    "occurred_at": datetime.now().isoformat(),
    "actor": {
        "type": "user",
        "id": "user_01GBNJC3MX9ZZJW1FSTF4C5938",
    },
    "targets": [
        {
            "type": "team",
            "id": "team_01GBNJD4MKHVKJGEWK42JNMBGS",
        },
    ],
    "context": {
        "location": "123.123.123.123",
        "user_agent": "Chrome/104.0.0.0",
    },
}

user_logged_out = {
    "action": "user.logged_out",
    "occurred_at": datetime.now().isoformat(),
    "actor": {
        "type": "user",
        "id": "user_01GBNJC3MX9ZZJW1FSTF4C5938",
    },
    "targets": [
        {
            "type": "team",
            "id": "team_01GBNJD4MKHVKJGEWK42JNMBGS",
        },
    ],
    "context": {
        "location": "123.123.123.123",
        "user_agent": "Chrome/104.0.0.0",
    },
}

user_organization_set = {
    "action": "user.organization_set",
    "occurred_at": datetime.now().isoformat(),
    "actor": {
        "type": "user",
        "id": "user_01GBNJC3MX9ZZJW1FSTF4C5938",
    },
    "targets": [
        {
            "type": "team",
            "id": "team_01GBNJD4MKHVKJGEWK42JNMBGS",
        },
    ],
    "context": {
        "location": "123.123.123.123",
        "user_agent": "Chrome/104.0.0.0",
    },
}

user_organization_deleted = {
    "action": "user.organization_deleted",
    "occurred_at": datetime.now().isoformat(),
    "actor": {
        "type": "user",
        "id": "user_01GBNJC3MX9ZZJW1FSTF4C5938",
    },
    "targets": [
        {
            "type": "team",
            "id": "team_01GBNJD4MKHVKJGEWK42JNMBGS",
        },
    ],
    "context": {
        "location": "123.123.123.123",
        "user_agent": "Chrome/104.0.0.0",
    },
}

user_connection_deleted = {
    "action": "user.connection_deleted",
    "occurred_at": datetime.now().isoformat(),
    "actor": {
        "type": "user",
        "id": "user_01GBNJC3MX9ZZJW1FSTF4C5938",
    },
    "targets": [
        {
            "type": "team",
            "id": "team_01GBNJD4MKHVKJGEWK42JNMBGS",
        },
    ],
    "context": {
        "location": "123.123.123.123",
        "user_agent": "Chrome/104.0.0.0",
    },
}
