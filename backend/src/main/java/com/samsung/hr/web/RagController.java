package com.samsung.hr.web;

import com.samsung.hr.domain.RagDocument;
import com.samsung.hr.service.RagService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/rag")
public class RagController {

    private final RagService ragService;

    public RagController(RagService ragService) {
        this.ragService = ragService;
    }

    @PostMapping("/documents")
    @ResponseStatus(HttpStatus.CREATED)
    public RagDocument upload(@RequestParam("file") MultipartFile file) throws IOException {
        return ragService.upload(file);
    }

    @GetMapping("/documents")
    public List<RagDocument> list() {
        return ragService.list();
    }
}
