{{/* Chart name */}}
{{- define "flight-review.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Fully qualified app name */}}
{{- define "flight-review.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "flight-review.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "flight-review.labels" -}}
helm.sh/chart: {{ include "flight-review.chart" . }}
{{ include "flight-review.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: flight-review
{{- end }}

{{- define "flight-review.selectorLabels" -}}
app.kubernetes.io/name: {{ include "flight-review.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: app
{{- end }}

{{- define "flight-review.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "flight-review.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/* Image reference: digest wins over tag */}}
{{- define "flight-review.image" -}}
{{- if .Values.image.digest }}
{{- printf "%s@%s" .Values.image.repository .Values.image.digest }}
{{- else }}
{{- printf "%s:%s" .Values.image.repository (default .Chart.AppVersion .Values.image.tag) }}
{{- end }}
{{- end }}

{{- define "flight-review.configSecretName" -}}
{{- default (printf "%s-config" (include "flight-review.fullname" .)) .Values.secrets.existingSecret }}
{{- end }}

{{/* Rendered config_user.ini */}}
{{- define "flight-review.configIni" -}}
[general]
domain_name = {{ .Values.domain }}
http_protocol = {{ .Values.config.httpProtocol }}
storage_path = /opt/data
db_filename =
airframes_url = {{ .Values.config.airframesUrl }}
parameters_url = {{ .Values.config.parametersUrl }}
events_url = {{ .Values.config.eventsUrl }}
cesium_api_key = {{ .Values.secrets.cesiumApiKey }}
mapbox_api_access_token = {{ .Values.secrets.mapboxApiAccessToken }}
cesium_enable_bing_aerial = {{ .Values.config.cesiumEnableBingAerial }}
log_cache_size = {{ .Values.config.logCacheSize }}
log_load_timeout = {{ .Values.config.logLoadTimeout }}
{{- if .Values.secrets.ulgePrivateKey }}
ulge_private_key = /opt/service/private_key/private_key.pem
{{- else }}
ulge_private_key =
{{- end }}

[debug]
print_timing = 0
verbose_output = 0

[email]
smtpserver = {{ .Values.config.email.smtpServer }}
sender     = {{ .Values.config.email.sender }}
user_name  = {{ .Values.config.email.userName }}
password   = {{ .Values.secrets.smtpPassword }}

[email_notifications]
public_flightreport = {{ .Values.config.notifications.publicFlightreport }}
public_flightreport_bad = {{ .Values.config.notifications.publicFlightreportBad }}
{{- with .Values.config.extra }}

{{ . }}
{{- end }}
{{- end }}
