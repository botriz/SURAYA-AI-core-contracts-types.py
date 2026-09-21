# SURAYA AI — CLOUD STORAGE

## هدف

SURAYA باید بتواند در کنار حافظه و فایل‌های محلی، از
فضای ذخیره‌سازی ابری نیز استفاده کند.

## معماری

Cloud Storage باید به صورت Adapter پیاده‌سازی شود.

Core نباید مستقیماً به یک سرویس ابری وابسته باشد.

## قرارداد پایه

هر Provider باید در نهایت این عملیات را پشتیبانی کند:

- upload
- download
- delete
- list
- exists
- metadata

## Providerهای آینده

- Google Drive
- Microsoft OneDrive
- Dropbox
- Amazon S3
- Cloudflare R2
- S3 Compatible Storage
- Private Server
- NAS
- Self Hosted Object Storage

## امنیت

اطلاعات دسترسی نباید در کد اصلی ذخیره شوند.

Credentialها باید در Secret Vault رمزنگاری‌شده نگهداری شوند.

دسترسی‌ها باید حداقل سطح دسترسی لازم را داشته باشند.

عملیات حساس باید قبل از اجرا توسط Guardian بررسی شوند.

## اصل مهم

Cloud Storage جایگزین کامل حافظه محلی نیست.

SURAYA باید بتواند در صورت قطع اینترنت:

- Core را اجرا کند
- حافظه محلی را بخواند
- Audit را ثبت کند
- عملیات مجاز محلی را انجام دهد

پس از اتصال مجدد، سیستم می‌تواند عملیات همگام‌سازی را انجام دهد.

## وضعیت

این قرارداد برای اتصال Providerهای واقعی آماده شده است.
