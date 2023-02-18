/*
 * File Name :    main.py
 * Author    :    qingshang
 * QQ        :    2918720083
 * Date      :    2022年3月18日 23点04分
 */
/* TODO: 2022年3月18日 23点04分 测试无异常 */
const startTime = (new Date).getTime(),
    generator = require("@babel/generator"),
    parser = require("@babel/parser"),
    traverse = require("@babel/traverse"),
    t = require("@babel/types"),
    fs = require("fs"),
    file_name = "eval.js",
    path = __dirname,
    input_path = path + "\\input\\" + file_name,
    output_path = path + "\\out\\de_" + file_name,
    js = String(fs.readFileSync(input_path, {
        encoding: "utf-8"
    }));
let ast = parser.parse(js);

function reload(ast) {
    const code = generator.default(ast, {
        minimal: !0,
        compact: !0
    }).code;
    return parser.parse(code)
}
const replace_function = {
        FunctionDeclaration(path) {
            const {
                id: id,
                body: body
            } = path.node;
            if (t.isReturnStatement(body.body[0]) && t.isLiteral(body.body[0].argument)) {
                const fun_name = id.name,
                    binding = path.scope.getBinding(fun_name),
                    value = body.body[0].argument.value;
                binding && 0 === binding.constantViolations.length && binding.referencePaths.map((function (referencePaths) {
                    referencePaths.parentPath.replaceWith(t.valueToNode(value))
                })), path.remove()
            }
        }
    },
    rs_while = {
        WhileStatement: function (path) {
            const {
                test: test,
                body: body
            } = path.node;
            if (!t.isLiteral(test) || 1 !== test.value) return;
            const path_PrevSibling = path.getPrevSibling();
            if (!t.isVariableDeclaration(path_PrevSibling) || !t.isArrayExpression(path_PrevSibling.node.declarations.slice(-1)[0].init)) return;
            let array_list_node = path_PrevSibling.node.declarations.slice(-1)[0].init.elements;
            const path_index = path_PrevSibling.node.declarations.slice(-2, -1)[0],
                index_node = path_index.init,
                index_name = path_index.id.name;
            let array_list = [];
            if (t.isNumericLiteral(index_node)) array_list.push(index_node.extra.rawValue);
            else if (t.isIdentifier(index_node)) {
                let fun_name = path.getFunctionParent().node.id.name;
                const binding = path.getFunctionParent().scope.getBinding(fun_name);
                binding && 0 === binding.constantViolations.length && binding.referencePaths.map((function (referencePaths) {
                    if (t.isCallExpression(referencePaths.parentPath)) {
                        let tmp_value = referencePaths.parentPath.node.arguments[0].extra.rawValue;
                        array_list.indexOf(tmp_value) < 0 && array_list.push(tmp_value)
                    } else console.log("replace", referencePaths.parentPath.parentPath + "")
                }))
            }
            array_list.sort((function (a, b) {
                return a - b
            }));
            let index_var_name = body.body[0].expression.left.name,
                if_body = body.body[1],
                sw_case = [];
            for (let index of array_list) {
                console.log(`当前${index} - arrlist ${array_list_node[index].value}`);
                let tmp_index = index,
                    tmp_body = [];
                for (;;) {
                    let init_index, re_body = body_index(if_body, array_list_node[tmp_index++].value, index_var_name);
                    if (re_body) {
                        if (t.isIfStatement(re_body)) {
                            let if_true_body = if_true(re_body, array_list_node, tmp_index, if_body, index_var_name, index_name),
                                if_false_body = if_false(re_body, array_list_node, tmp_index, if_body, index_var_name, index_name),
                                tmp_true_body = if_true_body,
                                tmp_false_body = if_false_body;
                            for (let index = 0; index < if_false_body.length; index++)
                                if (arrayEqual(if_false_body.slice(index), if_true_body)) {
                                    tmp_true_body = if_false_body.slice(index), tmp_false_body = if_false_body.slice(0, index);
                                    break
                                } let tmp_consequent = t.blockStatement([]),
                                tmp_alternate = t.blockStatement(tmp_false_body);
                            tmp_body.push(t.ifStatement(re_body.test, tmp_consequent, tmp_alternate)), tmp_body = tmp_body.concat(tmp_true_body);
                            break
                        }
                        if (re_body && re_body.expression && re_body.expression.left && re_body.expression.left.name === index_name) tmp_index = get_index(re_body, tmp_index);
                        else if (tmp_body.push(re_body), t.isReturnStatement(re_body)) break
                    }
                }
                tmp_body.push(t.breakStatement()), sw_case.push(t.switchCase(t.valueToNode(index), tmp_body))
            }
            let default_tmp = [];
            default_tmp.push(t.ExpressionStatement(t.callExpression(t.MemberExpression(t.Identifier("console"), t.Identifier("log")), [t.identifier(index_name)]))), default_tmp.push(t.ExpressionStatement(t.callExpression(t.identifier("alert"), [t.valueToNode("error")]))), default_tmp.push(t.breakStatement()), sw_case.push(t.switchCase(null, default_tmp)), path.replaceWith(t.SwitchStatement(t.identifier(index_name), sw_case))
        }
    };

function get_index(re_body, index) {
    let add_value;
    add_value = re_body.expression.right.operator ? re_body.expression.right.operator + re_body.expression.right.argument.value : re_body.expression.right.value;
    let eval_tmp = 0;
    return eval("eval_tmp" + re_body.expression.operator + add_value), index + eval_tmp
}

function body_index(if_body, init_index, index_var_name) {
    let {
        test: test,
        consequent: consequent,
        alternate: alternate
    } = if_body;
    if (t.isBinaryExpression(test)) {
        let {
            operator: operator,
            right: right
        } = test;
        return eval(init_index + operator + right.value) ? t.isIfStatement(consequent.body[0]) ? body_index(consequent.body[0], init_index, index_var_name) : consequent.body[0] : t.isIfStatement(alternate) ? body_index(alternate, init_index, index_var_name) : t.isIfStatement(alternate.body[0]) ? body_index(alternate.body[0], init_index, index_var_name) : alternate.body[0]
    }
    return if_body
}

function if_true(re_body, array_list_node, tmp_params_index, if_body, index_var_name, index_name) {
    let {
        consequent: consequent
    } = re_body, tmp_index = get_index(consequent, tmp_params_index), tmp_body = [];
    for (;;) {
        let init_index, re_body = body_index(if_body, array_list_node[tmp_index++].value, index_var_name);
        if (re_body) {
            if (t.isIfStatement(re_body)) {
                let if_true_body = if_true(re_body, array_list_node, tmp_index, if_body, index_var_name, index_name),
                    if_false_body = if_false(re_body, array_list_node, tmp_index, if_body, index_var_name, index_name),
                    tmp_true_body = if_true_body,
                    tmp_false_body = if_false_body;
                for (let index = 0; index < if_false_body.length; index++)
                    if (arrayEqual(if_false_body.slice(index), if_true_body)) {
                        tmp_true_body = if_false_body.slice(index), tmp_false_body = if_false_body.slice(0, index);
                        break
                    } let tmp_consequent = t.blockStatement([]),
                    tmp_alternate = t.blockStatement(tmp_false_body);
                tmp_body.push(t.ifStatement(re_body.test, tmp_consequent, tmp_alternate)), tmp_body = tmp_body.concat(tmp_true_body);
                break
            }
            if (re_body && re_body.expression && re_body.expression.left && re_body.expression.left.name === index_name) tmp_index = get_index(re_body, tmp_index);
            else if (tmp_body.push(re_body), t.isReturnStatement(re_body)) break
        }
    }
    return tmp_body
}

function if_false(re_body, array_list_node, tmp_params_index, if_body, index_var_name, index_name) {
    let tmp_body = [],
        tmp_index = tmp_params_index;
    for (;;) {
        let init_index, re_body = body_index(if_body, array_list_node[tmp_index++].value, index_var_name);
        if (re_body) {
            if (t.isIfStatement(re_body)) {
                let if_true_body = if_true(re_body, array_list_node, tmp_index, if_body, index_var_name, index_name),
                    if_false_body = if_false(re_body, array_list_node, tmp_index, if_body, index_var_name, index_name),
                    tmp_true_body = if_true_body,
                    tmp_false_body = if_false_body;
                for (let index = 0; index < if_false_body.length; index++)
                    if (arrayEqual(if_false_body.slice(index), if_true_body)) {
                        tmp_true_body = if_false_body.slice(index), tmp_false_body = if_false_body.slice(0, index);
                        break
                    } let tmp_consequent = t.blockStatement([]),
                    tmp_alternate = t.blockStatement(tmp_false_body);
                tmp_body.push(t.ifStatement(re_body.test, tmp_consequent, tmp_alternate)), tmp_body = tmp_body.concat(tmp_true_body);
                break
            }
            if (re_body && re_body.expression && re_body.expression.left && re_body.expression.left.name === index_name) tmp_index = get_index(re_body, tmp_index);
            else if (tmp_body.push(re_body), t.isReturnStatement(re_body)) break
        }
    }
    return tmp_body
}

function arrayEqual(arr1, arr2) {
    if (arr1 === arr2) return !0;
    if (arr1.length !== arr2.length) return !1;
    for (var i = 0; i < arr1.length; ++i)
        if (generator.default(arr1[i]).code !== generator.default(arr2[i]).code) return !1;
    return !0
}
const arrayStr = {
        StringLiteral(path) {
            function _$ac(_$WX) {
                for (var _$5_ = String.fromCharCode, _$5x = _$WX.length, _$ie, _$rX = new Array(_$5x - 1), _$ks = _$WX.charCodeAt(0) - 97, _$$C = 0, _$Fv = 1; _$Fv < _$5x; ++_$Fv)(_$ie = _$WX.charCodeAt(_$Fv)) >= 40 && _$ie < 92 ? (_$ie += _$ks) >= 92 && (_$ie -= 52) : _$ie >= 97 && _$ie < 127 && (_$ie += _$ks) >= 127 && (_$ie -= 30), _$rX[_$$C++] = _$ie;
                return _$5_.apply(null, _$rX)
            }

            function _$5x(_$WX) {
                var _$5x = String.fromCharCode(96);
                return _$ac(_$WX).split(_$5x)
            }
            const {
                value: value
            } = path.node;
            if (value.length < 3e3) return;
            let PrevPath = path.getStatementParent().getPrevSibling();
            if (!t.isVariableDeclaration(PrevPath)) return;
            const {
                declarations: declarations
            } = PrevPath.node, arrayName = declarations[0].id.name, TempArrayStr = _$5x(value), getBindName = path.scope.getBinding(arrayName);
            getBindName.referencePaths.map((function (referencePath) {
                let member_path = referencePath.findParent(p => p.isMemberExpression());
                if (!member_path) return;
                let property = member_path.get("property");
                if (property.isNumericLiteral()) try {
                    member_path.replaceWith(t.valueToNode(TempArrayStr[property]))
                } catch (e) {}
            }))
        }
    },
    replace_VariableDeclarator = {
        VariableDeclarator(path) {
            const {
                id: id,
                init: init
            } = path.node;
            if (t.isIdentifier(init)) {
                const binding = path.scope.getBinding(id.name);
                if (binding && 0 === binding.constantViolations.length) try {
                    path.scope.rename(id.name, init.name, path.scope.block), path.remove()
                } catch (e) {
                    console.log("替换变量名", id.name, init.name)
                }
            } else if (t.isLiteral(init)) {
                const binding = path.scope.getBinding(id.name);
                binding && 0 === binding.constantViolations.length && (binding.referencePaths.map((function (referencePath) {
                    referencePath.replaceInline(init)
                })), path.remove())
            }
        }
    },
    replace_array = {
        VariableDeclarator(path) {
            const {
                id: id,
                init: init
            } = path.node;
            if (!t.isArrayExpression(init) || 0 === init.elements.length) return;
            let elements = init.elements;
            const binding = path.scope.getBinding(id.name);
            if (binding)
                for (const ref_path of binding.referencePaths) {
                    let member_path = ref_path.findParent(p => p.isMemberExpression());
                    if (!member_path) return;
                    let property = member_path.get("property");
                    if (!property.isNumericLiteral()) continue;
                    let index, arr_ele = elements[property.node.value];
                    try {
                        member_path.replaceWith(arr_ele)
                    } catch (e) {}
                }
        }
    },
    replace_evaluate = {
        BinaryExpression(path) {
            const {
                confident: confident,
                value: value
            } = path.evaluate();
            confident && path.replaceWith(t.valueToNode(value))
        }
    };
traverse.default(ast, replace_VariableDeclarator), traverse.default(ast, replace_array), traverse.default(ast, replace_function), traverse.default(ast, replace_evaluate), ast = reload(ast), traverse.default(ast, rs_while), ast = reload(ast),
input_path.indexOf("eval") > -1 && (traverse.default(ast, arrayStr), ast = reload(ast)); // 需替换前eval $ts数组
let code = generator.default(ast, {
    minimal: !1,
    compact: !0
}).code;
fs.writeFileSync(output_path, code, (function (err) {
    err && console.error(err)
})), console.log(">>>>>>>>>>>>>>>>>>RunTime " + ((new Date).getTime() - startTime) + "ms");
