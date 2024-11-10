"""init

Revision ID: 3efdb14fc9bf
Revises:
Create Date: 2024-11-03 20:39:51.832023

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3efdb14fc9bf"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("""
        CREATE TABLE comebacks (
            id VARCHAR(26) NOT NULL,
            date TIMESTAMP NOT NULL,
            artist VARCHAR(255) NOT NULL,
            album_title VARCHAR(255) NOT NULL,
            release VARCHAR(255),
            song_title VARCHAR(255),
            album_type VARCHAR(255),
            title_track VARCHAR(255),
            artist_type VARCHAR(255),

            CONSTRAINT comebacks_pk PRIMARY KEY (id),
            CONSTRAINT comebacks_id_uq UNIQUE (id)
        );

        CREATE INDEX comebacks_id_ix ON comebacks (id);
        CREATE INDEX comebacks_date_ix ON comebacks (date);
        CREATE INDEX comebacks_artist_ix ON comebacks (artist);
        
        CREATE TABLE schedule_subscribers (
            id VARCHAR(26) NOT NULL,
            guild_id BIGINT NOT NULL,
            channel_id BIGINT NOT NULL,
            message_id BIGINT,
            
            CONSTRAINT schedule_subscribers_pk PRIMARY KEY (id),
            CONSTRAINT schedule_subscribers_id_uq UNIQUE (id)    
        );
        
        CREATE INDEX schedule_subscribers_id_ix ON schedule_subscribers (id); 
        CREATE INDEX schedule_subscribers_message_id_ix ON schedule_subscribers (message_id); 
        """)
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("""
        DROP INDEX schedule_subscribers_message_id_ix;
        DROP INDEX schedule_subscribers_id_ix;
        DROP INDEX comebacks_artist_ix;
        DROP INDEX comebacks_date_ix;
        DROP INDEX comebacks_id_ix;

        DROP TABLE schedule_subscribers;  
        DROP TABLE comebacks;
        """)
    )
