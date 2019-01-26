// x86/x64 Runtime Code Generation Demonstration (Linux/macOS/Windows)
// Copyright (C) 2017 Jeffrey L. Overbey.
// Modifiend by Helvio Junior (M4v3r1ck)
// 
// Permission to use, copy, modify, and/or distribute this software for any
// purpose with or without fee is hereby granted.
// 
// THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
// WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
// SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
// WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
// OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
// CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
// Source: http://blog.jeff.over.bz/assembly/compilers/jit/2017/03/30/executing-dynamically-generated-machine-code.html

#if !defined(_WIN32) && !defined(_WIN64) ////////////////////////// Linux/macOS

#include <stddef.h>    // size_t
#include <stdint.h>    // uint8_t, uint32_t
#include <stdio.h>     // printf
#include <string.h>    // memcpy
#include <sys/mman.h>  // mmap, mprotect, munmap, MAP_FAILURE

// Machine code for "mov eax, 12345678h" followed by "ret"
uint8_t machine_code[] = { 0xB8, 0x78, 0x56, 0x34, 0x12, 0xC3 };

int main(int argc, char **argv) {
    // Allocate a new page of memory, setting its protections to read+write
    void *mem = mmap(NULL, sizeof(machine_code), PROT_READ | PROT_WRITE,
        MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (mem == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    // Write the machine code into the newly allocated page
    memcpy(mem, machine_code, sizeof(machine_code));

    // Change the page protections to read+execute
    if (mprotect(mem, sizeof(machine_code), PROT_READ | PROT_EXEC) == -1) {
        perror("mprotect");
        return 2;
    }

    // Point a function pointer at the newly allocated page, then call it
    uint32_t(*fn)() = (uint32_t(*)()) mem;
    uint32_t result = fn();
    printf("result = 0x%x\n", result);

    // Free the memory
    if (munmap(mem, sizeof(machine_code)) == -1) {
        perror("munmap");
        return 3;
    }

    return 0;
}

#else // defined(_WIN32) || defined(_WIN64) /////////////////////////// Windows

#include <windows.h>
#include <stddef.h>    // size_t
#include <stdint.h>    // uint8_t, uint32_t
#include <stdio.h>     // printf
#include <memory.h>    // memcpy_s
#include <tchar.h>     // Must be included before strsafe.h
#include <strsafe.h>
#include <windows.h>

// Display the error message corresponding to GetLastError() in a message box.
static void DisplayError(LPTSTR failedFunctionName);

uint8_t machine_code[] = { 0xB8, 0x78, 0x56, 0x34, 0x12, 0xC3 };

int _tmain(int argc, _TCHAR **argv) {
    // Allocate a new page of memory, setting its protections to read+write
    LPVOID mem = VirtualAlloc(NULL, sizeof(machine_code),
        MEM_COMMIT, PAGE_READWRITE);
    if (mem == NULL) {
        DisplayError(TEXT("VirtualAlloc"));
        return 1;
    }

    // Write the machine code into the newly allocated page
    if (memcpy_s(mem, sizeof(machine_code), machine_code, sizeof(machine_code))) {
        DisplayError(TEXT("memcpy_s"));
        return 2;
    }

    // Change the page protections to read+execute
    DWORD ignore;
    if (!VirtualProtect(mem, sizeof(machine_code), PAGE_EXECUTE_READ, &ignore)) {
        DisplayError(TEXT("VirtualAlloc"));
        return 3;
    }

    // Flush the instruction cache
    if (!FlushInstructionCache(GetCurrentProcess(), mem, sizeof(machine_code))) {
        DisplayError(TEXT("FlushInstructionCache"));
        return 4;
    }

    // Point a function pointer at the newly allocated page, then call it
    uint32_t(*fn)() = (uint32_t(*)()) mem;
    uint32_t result = fn();
    _tprintf(TEXT("result = 0x%x\n"), result);

    // Free the memory
    if (!VirtualFree(mem, 0, MEM_RELEASE)) {
        DisplayError(TEXT("VirtualFree"));
        return 5;
    }

    return 0;
}

// from https://msdn.microsoft.com/en-us/library/windows/desktop/ms680582.aspx
static void DisplayError(LPTSTR failedFunctionName) {
    DWORD errorCode = GetLastError();
    LPVOID msgBufPtr;
    FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER
                      | FORMAT_MESSAGE_FROM_SYSTEM
                      | FORMAT_MESSAGE_IGNORE_INSERTS,
                  NULL,
                  errorCode,
                  MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                  (LPTSTR)&msgBufPtr,
                  0,
                  NULL);

    size_t size = sizeof(TCHAR) * (lstrlen((LPCTSTR)msgBufPtr)
                                   + lstrlen((LPCTSTR)failedFunctionName)
                                   + 40 /* Static text below */);
    LPVOID displayBufPtr = (LPVOID)LocalAlloc(LMEM_ZEROINIT, size);
    StringCchPrintf((LPTSTR)displayBufPtr,
                    LocalSize(displayBufPtr) / sizeof(TCHAR),
                    TEXT("%s failed with error %d: %s"),
                    failedFunctionName,
                    errorCode,
                    msgBufPtr);
    MessageBox(NULL, (LPCTSTR)displayBufPtr, TEXT("Error"), MB_ICONERROR);

    LocalFree(msgBufPtr);
    LocalFree(displayBufPtr);
}

#endif
