from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Check database status and run migrations if needed'

    def handle(self, *args, **options):
        self.stdout.write("Checking database status...")
        
        try:
            # Test basic database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS("Database connection: OK"))
            
            # Check if auth_user table exists
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'auth_user'
                    );
                """)
                table_exists = cursor.fetchone()[0]
                
            if table_exists:
                self.stdout.write(self.style.SUCCESS("auth_user table: EXISTS"))
            else:
                self.stdout.write(self.style.WARNING("auth_user table: DOES NOT EXIST"))
                self.stdout.write("Running migrations...")
                call_command('migrate', verbosity=2)
                
                # Check again after migration
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'auth_user'
                        );
                    """)
                    table_exists_after = cursor.fetchone()[0]
                    
                if table_exists_after:
                    self.stdout.write(self.style.SUCCESS("auth_user table created successfully"))
                else:
                    self.stdout.write(self.style.ERROR("Failed to create auth_user table"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Database error: {str(e)}")) 