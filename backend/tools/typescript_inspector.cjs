
const ts = require("typescript");
const fs = require("node:fs");

function inspectSource(filePath, code) {
    const extension = filePath.split(".").pop().toLowerCase();

    const scriptKind = {
        ts: ts.ScriptKind.TS,
        tsx: ts.ScriptKind.TSX,
        js: ts.ScriptKind.JS,
        jsx: ts.ScriptKind.JSX
    }[extension] ?? ts.ScriptKind.Unknown;

    const sourceFile = ts.createSourceFile(
        filePath,
        code,
        ts.ScriptTarget.Latest,
        true,
        scriptKind
    );

    const functions = [];
    const classes = [];
    const imports = [];

    function visit(node) {
        if (ts.isFunctionDeclaration(node) && node.name) {
            functions.push(node.name.text);
        }

        if (ts.isMethodDeclaration(node) && node.name) {
            functions.push(node.name.getText(sourceFile));
        }

        if (ts.isClassDeclaration(node) && node.name) {
            classes.push(node.name.text);
        }

        if (
    ts.isImportDeclaration(node) &&
    ts.isStringLiteral(node.moduleSpecifier)
     ) {
    imports.push({
        module: node.moduleSpecifier.text,
        type: "import"
    });
}

        ts.forEachChild(node, visit);
    }

    visit(sourceFile);

    const errors = sourceFile.parseDiagnostics.map(error => ({
        line: sourceFile.getLineAndCharacterOfPosition(
            error.start ?? 0
        ).line + 1,
        message: ts.flattenDiagnosticMessageText(
            error.messageText,
            "\n"
        )
    }));

    return {
        language: ["ts", "tsx"].includes(extension)
            ? "typescript"
            : "javascript",
        syntax_valid: errors.length === 0,
        functions,
        classes,
        imports,
        errors
    };
}

try {
    const input = JSON.parse(fs.readFileSync(0, "utf8"));

    if (
        typeof input.file_path !== "string" ||
        typeof input.code !== "string"
    ) {
        throw new Error("Invalid inspector input.");
    }

    console.log(JSON.stringify(
        inspectSource(input.file_path, input.code)
    ));
} catch (error) {
    console.error(error.message);
    process.exitCode = 1;
}
