// Tests de protocole de cdx_bus.h : cl /EHsc /std:c++17 test_bus.cpp && test_bus.exe
// Rien ne touche aux vrais réglages ni au vrai bus : dossier temporaire (CDX_SUITE_DIR) et préfixe de tube de test (CDX_PIPE_PREFIX).
#include "cdx_bus.h"
#include <cstdio>
#include <thread>
#include <vector>

static int g_bad = 0;
static void Check(const char* what, bool ok) { printf("%s  %s\n", ok ? "OK    " : "ECHEC ", what); if (!ok) ++g_bad; }

static void WriteFileText(const std::wstring& path, const std::string& text) {
    HANDLE h = CreateFileW(path.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    DWORD n; WriteFile(h, text.data(), static_cast<DWORD>(text.size()), &n, nullptr); CloseHandle(h);
}

int main() {
    using namespace cdx;
    // ---- Compose
    Check("Compose : enveloppe type/from/data", bus::Compose("open-url", "kirc", "{\"url\":\"https://example.org/\"}") == "{\"type\":\"open-url\",\"from\":\"kirc\",\"data\":{\"url\":\"https://example.org/\"}}");
    Check("Compose : data absent -> {}", bus::Compose("audio.get", "shell") == "{\"type\":\"audio.get\",\"from\":\"shell\",\"data\":{}}");
    Check("Compose : guillemets et retours à la ligne échappés dans le type", bus::Compose("a\"b\n", "x").find('\n') == std::string::npos);
    Check("IsApp : liste blanche des noms", bus::IsApp("browser") && bus::IsApp("audiolinker") && !bus::IsApp("..\\evil") && !bus::IsApp(""));

    // ---- suite.json
    Check("ParseAccent : accent valide", suite::ParseAccent("{\"version\":1,\"accent\":\"bleu\"}") == "bleu");
    Check("ParseAccent : sans version, accepté", suite::ParseAccent("{\"accent\":\"vert\"}") == "vert");
    Check("ParseAccent : version 2 ignorée", suite::ParseAccent("{\"version\":2,\"accent\":\"bleu\"}", "ambre") == "ambre");
    Check("ParseAccent : version 12 ignorée", suite::ParseAccent("{\"version\":12,\"accent\":\"bleu\"}", "ambre") == "ambre");
    Check("ParseAccent : accent inconnu -> repli", suite::ParseAccent("{\"version\":1,\"accent\":\"../x\"}", "violet") == "violet");
    Check("ParseAccent : fichier abîmé -> repli", suite::ParseAccent("{{{ pas du json", "charbon") == "charbon");
    Check("ParseAccent : vide -> repli", suite::ParseAccent("", "rouge") == "rouge");

    wchar_t tmp[MAX_PATH]; GetTempPathW(MAX_PATH, tmp);
    std::wstring dir = std::wstring(tmp) + L"cdx-bus-test-" + std::to_wstring(GetCurrentProcessId());
    CreateDirectoryW(dir.c_str(), nullptr);
    SetEnvironmentVariableW(L"CDX_SUITE_DIR", dir.c_str());
    Check("ReadAccent : fichier absent -> repli", suite::ReadAccent("sarcelle") == "sarcelle");
    suite::Watcher w("rouge");
    std::string a;
    Check("Watcher : rien n'a changé", !w.Changed(a));
    WriteFileText(suite::Path(), "{\"version\":1,\"accent\":\"bleu\"}");
    Check("Watcher : nouveau fichier -> bleu", w.Changed(a) && a == "bleu");
    Check("Watcher : pas de second signal", !w.Changed(a));
    Sleep(30);
    WriteFileText(suite::Path(), "{\"version\":1,\"accent\":\"bleu\"}");
    Check("Watcher : fichier réécrit à l'identique -> pas de changement d'accent", !w.Changed(a));
    WriteFileText(suite::Path(), "n'importe quoi");
    Check("Watcher : fichier abîmé -> l'accent précédent est gardé", !w.Changed(a) && w.Current() == "bleu");
    WriteFileText(suite::Path(), "{\"version\":1,\"accent\":\"ambre\"}");
    Check("Watcher : retour à un fichier valide -> ambre", w.Changed(a) && a == "ambre");
    DeleteFileW(suite::Path().c_str()); RemoveDirectoryW(dir.c_str());

    // ---- Send contre un serveur de tube de test
    std::wstring prefix = L"cdxtest" + std::to_wstring(GetCurrentProcessId()) + L".";
    SetEnvironmentVariableW(L"CDX_PIPE_PREFIX", prefix.c_str());
    Check("Send : application qui n'écoute pas -> false", !bus::Send("browser", "open-url", "{}"));
    Check("Send : nom inconnu -> false", !bus::Send("nimporte", "x"));
    std::wstring pipeName = L"\\\\.\\pipe\\" + prefix + L"browser";
    HANDLE srv = CreateNamedPipeW(pipeName.c_str(), PIPE_ACCESS_INBOUND, PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT | PIPE_REJECT_REMOTE_CLIENTS, 2, 4096, 4096, 0, nullptr);
    std::string got;
    HANDLE ready = CreateEventW(nullptr, TRUE, FALSE, nullptr);
    std::thread th([&] {
        SetEvent(ready);   // le serveur attend déjà la connexion quand le client arrive, comme dans les vrais programmes
        if (ConnectNamedPipe(srv, nullptr) || GetLastError() == ERROR_PIPE_CONNECTED) {
            char buf[1024]; DWORD n = 0;
            while (ReadFile(srv, buf, sizeof(buf), &n, nullptr) && n) got.append(buf, n);
        }
    });
    WaitForSingleObject(ready, 2000); Sleep(100);
    bool sent = bus::Send("browser", "open-url", "{\"url\":\"https://example.org/\"}", "kirc");
    th.join();
    CloseHandle(srv);
    Check("Send : message écrit", sent);
    if (got.size() < 200) printf("      recu : [%s] (%zu octets)\n", got.c_str(), got.size());
    Check("Send : le serveur reçoit exactement une ligne d'enveloppe", got == "{\"type\":\"open-url\",\"from\":\"kirc\",\"data\":{\"url\":\"https://example.org/\"}}\n");
    std::string huge(kBusMaxLine, 'x');
    Check("Send : ligne de plus de 64 Ko refusée", !bus::Send("browser", "open-url", "{\"u\":\"" + huge + "\"}"));

    printf(g_bad == 0 ? "TOUT EST BON\n" : "%d verification(s) en echec\n", g_bad);
    return g_bad == 0 ? 0 : 1;
}
