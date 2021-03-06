from typing import TYPE_CHECKING, Any, Match, Union, List
from typing_extensions import Literal, Annotated
import re
from dataclasses import dataclass

from pydantic import Field
from pydantic.class_validators import validator, root_validator

from woke.e_ast_parsing.a_abc import AstAbc
from woke.e_ast_parsing.b_solc.a_ast_basic_types import *
from woke.e_ast_parsing.b_solc.b_ast_enums import *

REGEX_SRC = re.compile(r"(\d+):(\d+):(\d+)")
PYDANTIC_CONFIG_EXTRA = "forbid"
PYDANTIC_CONFIG_ALLOW_MUTATION = False


def to_camel(s: str) -> str:
    split = s.split("_")
    return split[0].lower() + "".join([w.capitalize() for w in split[1:]])


class ConfiguredModel(AstAbc):
    class Config:
        alias_generator = to_camel
        extra = PYDANTIC_CONFIG_EXTRA
        allow_mutation = PYDANTIC_CONFIG_ALLOW_MUTATION


SolcTopLevelMemberUnion = Annotated[
    Union[
        "SolcPragmaDirective",
        "SolcImportDirective",
        # new in solc X
        "SolcVariableDeclaration",
        "SolcEnumDefinition",
        "SolcFunctionDefinition",
        "SolcStructDefinition",
        "SolcErrorDefinition",
        # new in solc 0.8.8
        "SolcUserDefinedValueTypeDefinition",
        # everywhere
        "SolcContractDefinition",
    ],
    Field(discriminator="node_type"),
]

SolcContractMemberUnion = Annotated[
    Union[
        "SolcEnumDefinition",
        "SolcErrorDefinition",
        "SolcEventDefinition",
        "SolcFunctionDefinition",
        "SolcModifierDefinition",
        "SolcStructDefinition",
        "SolcUserDefinedValueTypeDefinition",
        "SolcUsingForDirective",
        "SolcVariableDeclaration",
    ],
    Field(discriminator="node_type"),
]

SolcLibraryNameUnion = Annotated[
    Union[
        "SolcUserDefinedTypeName",
        "SolcIdentifierPath",
    ],
    Field(discriminator="node_type"),
]

SolcTypeNameUnion = Annotated[
    Union[
        "SolcArrayTypeName",
        "SolcElementaryTypeName",
        "SolcFunctionTypeName",
        "SolcMapping",
        "SolcUserDefinedTypeName",
    ],
    Field(discriminator="node_type"),
]

OptionalSolcTypeNameUnion = Annotated[
    Union[
        "SolcArrayTypeName",
        "SolcElementaryTypeName",
        "SolcFunctionTypeName",
        "SolcMapping",
        "SolcUserDefinedTypeName",
        None,
    ],
    Field(discriminator="node_type"),
]

SolcExpressionUnion = Annotated[
    Union[
        "SolcAssignment",
        "SolcBinaryOperation",
        "SolcConditional",
        "SolcElementaryTypeNameExpression",
        "SolcFunctionCall",
        "SolcFunctionCallOptions",
        "SolcIdentifier",
        "SolcIndexAccess",
        "SolcIndexRangeAccess",
        "SolcLiteral",
        "SolcMemberAccess",
        "SolcNewExpression",
        "SolcTupleExpression",
        "SolcUnaryOperation",
    ],
    Field(discriminator="node_type"),
]

OptionalSolcExpressionUnion = Annotated[
    Union[
        "SolcAssignment",
        "SolcBinaryOperation",
        "SolcConditional",
        "SolcElementaryTypeNameExpression",
        "SolcFunctionCall",
        "SolcFunctionCallOptions",
        "SolcIdentifier",
        "SolcIndexAccess",
        "SolcIndexRangeAccess",
        "SolcLiteral",
        "SolcMemberAccess",
        "SolcNewExpression",
        "SolcTupleExpression",
        "SolcUnaryOperation",
        None,
    ],
    Field(discriminator="node_type"),
]

SolcInitExprUnion = Annotated[
    Union[
        "SolcExpressionStatement",
        "SolcVariableDeclarationStatement",
    ],
    Field(discriminator="node_type"),
]

OptionalSolcInitExprUnion = Annotated[
    Union[
        "SolcExpressionStatement",
        "SolcVariableDeclarationStatement",
    ],
    Field(discriminator="node_type"),
]

SolcStatementUnion = Annotated[
    Union[
        "SolcBlock",
        "SolcBreak",
        "SolcContinue",
        "SolcDoWhileStatement",
        "SolcEmitStatement",
        "SolcExpressionStatement",
        "SolcForStatement",
        "SolcIfStatement",
        "SolcInlineAssembly",
        "SolcPlaceholderStatement",
        "SolcReturn",
        "SolcRevertStatement",
        "SolcTryStatement",
        # 'SolcUncheckedBlock',
        "SolcVariableDeclarationStatement",
        "SolcWhileStatement",
    ],
    Field(discriminator="node_type"),
]

OptionalSolcStatementUnion = Annotated[
    Union[
        "SolcBlock",
        "SolcBreak",
        "SolcContinue",
        "SolcDoWhileStatement",
        "SolcEmitStatement",
        "SolcExpressionStatement",
        "SolcForStatement",
        "SolcIfStatement",
        "SolcInlineAssembly",
        "SolcPlaceholderStatement",
        "SolcReturn",
        "SolcRevertStatement",
        "SolcTryStatement",
        # 'SolcUncheckedBlock',
        "SolcVariableDeclarationStatement",
        "SolcWhileStatement",
        None,
    ],
    Field(discriminator="node_type"),
]

YulStatementUnion = Annotated[
    Union[
        "YulAssignment",
        "YulBlock",
        "YulBreak",
        "YulContinue",
        "YulExpressionStatement",
        "YulLeave",
        "YulForLoop",
        "YulFunctionDefinition",
        "YulIf",
        "YulSwitch",
        "YulVariableDeclaration",
    ],
    Field(discriminator="node_type"),
]

YulExpressionUnion = Annotated[
    Union[
        "YulFunctionCall",
        "YulIdentifier",
        "YulLiteral",
    ],
    Field(discriminator="node_type"),
]

OptionalYulExpressionUnion = Annotated[
    Union[
        "YulFunctionCall",
        "YulIdentifier",
        "YulLiteral",
        None,
    ],
    Field(discriminator="node_type"),
]

# ModifierInvocation
ModifierName = Annotated[
    Union["SolcIdentifier", "SolcIdentifierPath"],
    Field(discriminator="node_type"),
]

# InheritanceSpecifier
BaseName = Annotated[
    Union["SolcUserDefinedTypeName", "SolcIdentifierPath"],
    Field(discriminator="node_type"),
]

Override = Annotated[
    Union[
        "SolcUserDefinedTypeName",
        "SolcIdentifierPath",
    ],
    Field(discriminator="node_type"),
]


class TypeDescriptionsModel(ConfiguredModel):
    type_identifier: Optional[StrictStr]
    type_string: Optional[StrictStr]


class SymbolAliasModel(ConfiguredModel):  # helper class
    foreign: "SolcIdentifier"
    local: Optional[StrictStr]
    name_location: Optional[NameLocation]


# InlineAssembly
class ExternalReferenceModel(ConfiguredModel):  # helper class
    declaration: AstNodeId
    is_offset: StrictBool
    is_slot: StrictBool
    src: Src
    value_size: StrictInt
    suffix: Optional[InlineAssemblySuffix]


@dataclass
class SrcParsed:
    byte_offset: int
    byte_length: int
    file_id: int


class SolcOrYulNode(ConfiguredModel):
    src: Src

    @validator("src")
    def parse_src(cls, src: Src) -> SrcParsed:
        res = re.search(REGEX_SRC, src)
        assert isinstance(res, Match), "Bad src"
        [m1, m2, m3] = [int(res.group(i)) for i in range(1, 4)]
        return SrcParsed(m1, m2, m3)


class SolcNode(SolcOrYulNode):
    id: AstNodeId

    def __iter__(self):
        def iter_list(l: List):
            for item in l:
                if isinstance(item, SolcNode):
                    yield item
                    yield from item
                elif isinstance(item, List):
                    yield from iter_list(item)

        for item in self.__dict__.values():
            if isinstance(item, SolcNode):
                yield item
                yield from item
            elif isinstance(item, List):
                yield from iter_list(item)


class YulNode(SolcOrYulNode):
    pass


class SolcSourceUnit(SolcNode):
    # override alias
    node_type: Literal["SourceUnit"] = Field(alias="nodeType")
    # required
    absolute_path: AbsolutePath
    exported_symbols: ExportedSymbols
    nodes: List[SolcTopLevelMemberUnion]
    # optional
    license: Optional[License]


# todo: replace by __root__
AstSolc = SolcSourceUnit


class SolcPragmaDirective(SolcNode):
    # override alias
    node_type: Literal["PragmaDirective"] = Field(alias="nodeType")
    literals: Literals


class SolcImportDirective(SolcNode):
    # override alias
    node_type: Literal["ImportDirective"] = Field(alias="nodeType")
    # required
    absolute_path: AbsolutePath
    file: File
    scope: AstNodeId
    source_unit: AstNodeId
    symbol_aliases: List[SymbolAliasModel]
    unit_alias: UnitAlias
    # optional
    name_location: Optional[NameLocation]


class SolcVariableDeclaration(SolcNode):
    # required
    # override alias
    node_type: Literal["VariableDeclaration"] = Field(alias="nodeType")
    name: Name
    constant: Constant
    mutability: Mutability
    scope: AstNodeId
    state_variable: StateVariable
    storage_location: StorageLocation
    type_descriptions: "TypeDescriptionsModel"
    visibility: Visibility
    # optional
    name_location: Optional[NameLocation]
    base_functions: Optional[BaseFunctions]
    documentation: Optional["SolcStructuredDocumentation"]
    function_selector: Optional[StrictStr]
    indexed: Optional[Indexed]
    overrides: Optional["SolcOverrideSpecifier"]
    type_name: OptionalSolcTypeNameUnion
    value: OptionalSolcExpressionUnion


class SolcEnumDefinition(SolcNode):
    # override alias
    node_type: Literal["EnumDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    canonical_name: CanonicalName
    members: List["SolcEnumValue"]
    # optional
    name_location: Optional[NameLocation]


class SolcFunctionDefinition(SolcNode):
    # override alias
    node_type: Literal["FunctionDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    implemented: Implemented
    kind: FunctionKind
    modifiers: List["SolcModifierInvocation"]
    parameters: "SolcParameterList"
    return_parameters: "SolcParameterList"
    scope: AstNodeId
    state_mutability: StateMutability
    virtual: Virtual
    visibility: Visibility
    # optional
    name_location: Optional[NameLocation]
    base_functions: Optional[BaseFunctions]
    documentation: Optional["SolcStructuredDocumentation"]
    function_selector: Optional[FunctionSelector]
    body: Optional["SolcBlock"]
    overrides: Optional["SolcOverrideSpecifier"]


class SolcStructDefinition(SolcNode):
    # override alias
    node_type: Literal["StructDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    canonical_name: CanonicalName
    members: List["SolcVariableDeclaration"]
    scope: AstNodeId
    visibility: Visibility
    # optional
    name_location: Optional[NameLocation]


class SolcErrorDefinition(SolcNode):
    # override alias
    node_type: Literal["ErrorDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    name_location: NameLocation
    parameters: "SolcParameterList"
    # optional
    documentation: Optional["SolcStructuredDocumentation"]


class SolcUserDefinedValueTypeDefinition(SolcNode):
    # override alias
    node_type: Literal["UserDefinedValueTypeDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    underlying_type: SolcTypeNameUnion
    # optional
    name_location: Optional[NameLocation]
    canonical_name: Optional[CanonicalName]


class SolcContractDefinition(SolcNode):
    # override alias
    node_type: Literal["ContractDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    abstract: Abstract
    base_contracts: List["SolcInheritanceSpecifier"]
    contract_dependencies: ContractDependencies
    contract_kind: ContractKind
    fully_implemented: FullyImplemented
    linearized_base_contracts: LinearizedBaseContracts
    nodes: List[SolcContractMemberUnion]
    scope: AstNodeId
    # optional
    name_location: Optional[NameLocation]
    canonical_name: Optional[CanonicalName]
    documentation: Optional["SolcStructuredDocumentation"]
    used_errors: Optional[UsedErrors]


class SolcEventDefinition(SolcNode):
    # override alias
    node_type: Literal["EventDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    anonymous: Anonymous
    parameters: "SolcParameterList"
    # optional
    name_location: Optional[NameLocation]
    documentation: Optional["SolcStructuredDocumentation"]
    event_selector: Optional[
        str
    ]  # an example: "0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9"


class SolcModifierDefinition(SolcNode):
    # override alias
    node_type: Literal["ModifierDefinition"] = Field(alias="nodeType")
    # required
    name: Name
    body: "SolcBlock"
    parameters: "SolcParameterList"
    virtual: Virtual
    visibility: Visibility
    # optional
    name_location: Optional[NameLocation]
    base_modifiers: Optional[BaseModifiers]
    documentation: Optional["SolcStructuredDocumentation"]
    overrides: Optional["SolcOverrideSpecifier"]


class SolcUsingForDirective(SolcNode):
    # override alias
    node_type: Literal["UsingForDirective"] = Field(alias="nodeType")
    # required
    # library_name: LibraryName
    library_name: SolcLibraryNameUnion
    type_name: SolcTypeNameUnion
    # optional


class SolcArrayTypeName(SolcNode):
    # override alias
    node_type: Literal["ArrayTypeName"] = Field(alias="nodeType")
    # required
    type_descriptions: TypeDescriptionsModel
    base_type: SolcTypeNameUnion
    # optional
    length: OptionalSolcExpressionUnion


class SolcElementaryTypeName(SolcNode):
    # override alias
    node_type: Literal["ElementaryTypeName"] = Field(alias="nodeType")
    # required
    type_descriptions: TypeDescriptionsModel
    name: Name
    # optional
    state_mutability: Optional[StateMutability]


class SolcFunctionTypeName(SolcNode):
    # override alias
    node_type: Literal["FunctionTypeName"] = Field(alias="nodeType")
    # required
    type_descriptions: TypeDescriptionsModel
    parameter_types: "SolcParameterList"
    return_parameter_types: "SolcParameterList"
    state_mutability: StateMutability
    visibility: Visibility
    # optional


class SolcMapping(SolcNode):
    # override alias
    node_type: Literal["Mapping"] = Field(alias="nodeType")
    # required
    type_descriptions: TypeDescriptionsModel
    key_type: SolcTypeNameUnion
    value_Type: SolcTypeNameUnion
    # optional


class SolcUserDefinedTypeName(SolcNode):
    node_type: Literal["UserDefinedTypeName"] = Field(alias="nodeType")
    # required
    type_descriptions: TypeDescriptionsModel
    referenced_declaration: ReferencedDeclaration
    # optional
    # TODO:
    contract_scope: Optional[AstNodeId]
    name: Optional[Name]
    path_node: Optional["SolcIdentifierPath"]


class SolcBlock(SolcNode):
    # override alias
    node_type: Literal["Block"] = Field(alias="nodeType")
    # required
    # optional
    # TODO:
    documentation: Optional[StrictStr]
    statements: Optional[List[SolcStatementUnion]]


class SolcBreak(SolcNode):
    # override alias
    node_type: Literal["Break"] = Field(alias="nodeType")
    # required
    # optional
    # TODO:
    documentation: Optional[StrictStr]


class SolcContinue(SolcNode):
    # override alias
    node_type: Literal["Continue"] = Field(alias="nodeType")
    # required
    # optional
    documentation: Optional[StrictStr]


class SolcDoWhileStatement(SolcNode):
    # override alias
    node_type: Literal["DoWhileStatement"] = Field(alias="nodeType")
    # required
    body: SolcStatementUnion
    condition: SolcExpressionUnion
    # optional
    documentation: Optional[StrictStr]


class SolcEmitStatement(SolcNode):
    # override alias
    node_type: Literal["EmitStatement"] = Field(alias="nodeType")
    # required
    event_call: "SolcFunctionCall"
    # optional
    documentation: Optional[StrictStr]


class SolcExpressionStatement(SolcNode):
    # override alias
    node_type: Literal["ExpressionStatement"] = Field(alias="nodeType")
    # required
    expression: SolcExpressionUnion
    # optional
    documentation: Optional[StrictStr]


class SolcForStatement(SolcNode):
    # override alias
    node_type: Literal["ForStatement"] = Field(alias="nodeType")
    # required
    body: SolcStatementUnion
    # optional
    documentation: Optional[StrictStr]
    condition: OptionalSolcExpressionUnion
    initialization_expression: OptionalSolcInitExprUnion
    loop_expression: "SolcExpressionStatement"


class SolcIfStatement(SolcNode):
    # override alias
    node_type: Literal["IfStatement"] = Field(alias="nodeType")
    # required
    condition: SolcExpressionUnion
    true_body: SolcStatementUnion
    # optional
    documentation: Optional[StrictStr]
    false_body: OptionalSolcStatementUnion


class SolcInlineAssembly(SolcNode):
    # override alias
    node_type: Literal["InlineAssembly"] = Field(alias="nodeType")
    # required
    # this one requires special care...
    ast: "YulBlock" = Field(..., alias="AST")
    evm_version: InlineAssemblyEvmVersion
    external_references: List[ExternalReferenceModel]
    # optional
    documentation: Optional[StrictStr]


class SolcPlaceholderStatement(SolcNode):
    # override alias
    node_type: Literal["PlaceholderStatement"] = Field(alias="nodeType")
    # required
    # optional
    documentation: Optional[StrictStr]


class SolcReturn(SolcNode):
    # override alias
    node_type: Literal["Return"] = Field(alias="nodeType")
    # required
    # optional
    function_return_parameters: Optional[FunctionReturnParameters]
    documentation: Optional[StrictStr]
    expression: OptionalSolcExpressionUnion


class SolcRevertStatement(SolcNode):
    # override alias
    node_type: Literal["RevertStatement"] = Field(alias="nodeType")
    # required
    error_call: "SolcFunctionCall"
    # optional
    documentation: Optional[StrictStr]


class SolcTryStatement(SolcNode):
    # override alias
    node_type: Literal["TryStatement"] = Field(alias="nodeType")
    # required
    clauses: List["SolcTryCatchClause"]
    external_call: "SolcFunctionCall"
    # optional
    documentation: Optional[StrictStr]


class SolcUncheckedBlock(SolcNode):
    # override alias
    node_type: Literal["UncheckedBlock"] = Field(alias="nodeType")
    # required
    statements: List[SolcStatementUnion]
    # optional
    documentation: Optional[StrictStr]


class SolcVariableDeclarationStatement(SolcNode):
    # override alias
    node_type: Literal["VariableDeclarationStatement"] = Field(alias="nodeType")
    # required
    assignments: Assignments
    declarations: List[Optional["SolcVariableDeclaration"]]
    # optional
    documentation: Optional[StrictStr]
    initial_value: OptionalSolcExpressionUnion


class SolcWhileStatement(SolcNode):
    # override alias
    node_type: Literal["WhileStatement"] = Field(alias="nodeType")
    # required
    body: SolcStatementUnion
    condition: SolcExpressionUnion
    # optional
    documentation: Optional[StrictStr]


class SolcAssignment(SolcNode):
    # override alias
    node_type: Literal["Assignment"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    left_hand_side: SolcExpressionUnion
    operator: AssignmentOperator
    right_hand_side: SolcExpressionUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcBinaryOperation(SolcNode):
    # override alias
    node_type: Literal["BinaryOperation"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    common_type: TypeDescriptionsModel
    left_expression: SolcExpressionUnion
    operator: BinaryOpOperator
    right_expression: SolcExpressionUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcConditional(SolcNode):
    # override alias
    node_type: Literal["Conditional"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    condition: SolcExpressionUnion
    false_expression: SolcExpressionUnion
    true_expression: SolcExpressionUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcElementaryTypeNameExpression(SolcNode):
    # override alias
    node_type: Literal["ElementaryTypeNameExpression"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    type_name: "SolcElementaryTypeName"
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcFunctionCall(SolcNode):
    # override alias
    node_type: Literal["FunctionCall"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    arguments: List[SolcExpressionUnion]
    expression: SolcExpressionUnion
    kind: FunctionCallKind
    names: Names
    try_call: TryCall
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcFunctionCallOptions(SolcNode):
    # override alias
    node_type: Literal["FunctionCallOptions"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    expression: SolcExpressionUnion
    names: Names
    options: List[SolcExpressionUnion]
    # optional
    # TODO:
    is_l_value: Optional[IsLValue]
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcIdentifier(SolcNode):
    # override alias
    node_type: Literal["Identifier"] = Field(alias="nodeType")
    # required
    name: Name
    overloaded_declarations: OverloadedDeclarations
    type_descriptions: TypeDescriptionsModel
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]
    referenced_declaration: Optional[ReferencedDeclaration]


class SolcIndexAccess(SolcNode):
    # override alias
    node_type: Literal["IndexAccess"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    base_expression: SolcExpressionUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]
    index_expression: OptionalSolcExpressionUnion  # example when this can be None: `abi.decode(params, (address[], uint256))`


class SolcIndexRangeAccess(SolcNode):
    # override alias
    node_type: Literal["IndexRangeAccess"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    base_expression: SolcExpressionUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]
    end_expression: OptionalSolcExpressionUnion
    start_expression: OptionalSolcExpressionUnion


class SolcLiteral(SolcNode):
    # override alias
    node_type: Literal["Literal"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    hex_value: HexValue
    kind: LiteralKind
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]
    subdenomination: Optional[StrictStr]  # can be for example "days" or "ether"
    value: Optional[Value]


class SolcMemberAccess(SolcNode):
    # override alias
    node_type: Literal["MemberAccess"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    expression: SolcExpressionUnion
    member_name: MemberName
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]
    referenced_declaration: Optional[ReferencedDeclaration]


class SolcNewExpression(SolcNode):
    # override alias
    node_type: Literal["NewExpression"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    type_name: SolcTypeNameUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]
    is_l_value: Optional[IsLValue]


class SolcTupleExpression(SolcNode):
    # override alias
    node_type: Literal["TupleExpression"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    components: List[OptionalSolcExpressionUnion]
    is_inline_array: IsInlineArray
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcUnaryOperation(SolcNode):
    # override alias
    node_type: Literal["UnaryOperation"] = Field(alias="nodeType")
    # required
    is_constant: IsConstant
    is_l_value: IsLValue
    is_pure: IsPure
    l_value_requested: LValueRequested
    type_descriptions: TypeDescriptionsModel
    operator: UnaryOpOperator
    prefix: Prefix
    sub_expression: SolcExpressionUnion
    # optional
    argument_types: Optional[List[TypeDescriptionsModel]]


class SolcOverrideSpecifier(SolcNode):
    # override alias
    node_type: Literal["OverrideSpecifier"] = Field(alias="nodeType")
    # required
    overrides: List[Override]
    # optional


class SolcIdentifierPath(SolcNode):
    node_type: Literal["IdentifierPath"] = Field(alias="nodeType")
    # required
    name: Name
    referenced_declaration: ReferencedDeclaration
    # optional


class SolcParameterList(SolcNode):
    # override alias
    node_type: Literal["ParameterList"] = Field(alias="nodeType")
    # required
    parameters: List["SolcVariableDeclaration"]
    # optional


class SolcTryCatchClause(SolcNode):
    # override alias
    node_type: Literal["TryCatchClause"] = Field(alias="nodeType")
    # required
    block: "SolcBlock"
    error_name: ErrorName
    # optional
    parameters: Optional["SolcParameterList"]


class SolcStructuredDocumentation(SolcNode):
    # override alias
    node_type: Literal["StructuredDocumentation"] = Field(alias="nodeType")
    # required
    text: Text
    # optional


class SolcEnumValue(SolcNode):
    # override alias
    node_type: Literal["EnumValue"] = Field(alias="nodeType")
    # required
    name: Name
    # optional
    name_location: Optional[NameLocation]


class SolcInheritanceSpecifier(SolcNode):
    # override alias
    node_type: Literal["InheritanceSpecifier"] = Field(alias="nodeType")
    # required
    base_name: BaseName
    # optional
    arguments: Optional[List[SolcExpressionUnion]]


class SolcModifierInvocation(SolcNode):
    # override alias
    node_type: Literal["ModifierInvocation"] = Field(alias="nodeType")
    # required
    modifier_name: ModifierName
    # optional
    arguments: Optional[List[SolcExpressionUnion]]
    kind: Optional[ModifierInvocationKind]


class YulAssignment(YulNode):
    # override alias
    node_type: Literal["YulAssignment"] = Field(alias="nodeType")
    # required
    value: "YulExpressionUnion"
    variable_names: List["YulIdentifier"]
    # optional


class YulBlock(YulNode):
    # override alias
    node_type: Literal["YulBlock"] = Field(alias="nodeType")
    # required
    statements: List["YulStatementUnion"]
    # optional


class YulBreak(YulNode):
    # override alias
    node_type: Literal["YulBreak"] = Field(alias="nodeType")
    # required
    # optional


class YulContinue(YulNode):
    # override alias
    node_type: Literal["YulContinue"] = Field(alias="nodeType")
    # required
    # optional


class YulExpressionStatement(YulNode):
    # override alias
    node_type: Literal["YulExpressionStatement"] = Field(alias="nodeType")
    # required
    expression: "YulExpressionUnion"
    # optional


class YulLeave(YulNode):
    # override alias
    node_type: Literal["YulLeave"] = Field(alias="nodeType")
    # required
    # optional


class YulForLoop(YulNode):
    # override alias
    node_type: Literal["YulForLoop"] = Field(alias="nodeType")
    # required
    body: "YulBlock"
    condition: "YulExpressionUnion"
    post: "YulBlock"
    pre: "YulBlock"
    # optional


class YulFunctionDefinition(YulNode):
    # override alias
    node_type: Literal["YulFunctionDefinition"] = Field(alias="nodeType")
    # required
    body: "YulBlock"
    name: Name
    parameters: List["YulTypedName"]
    return_variables: List["YulTypedName"]
    # optional


class YulIf(YulNode):
    # override alias
    node_type: Literal["YulIf"] = Field(alias="nodeType")
    # required
    body: "YulBlock"
    condition: "YulExpressionUnion"
    # optional


class YulSwitch(YulNode):
    # override alias
    node_type: Literal["YulSwitch"] = Field(alias="nodeType")
    # required
    cases: List["YulCase"]
    expression: "YulExpressionUnion"
    # optional


class YulVariableDeclaration(YulNode):
    # override alias
    node_type: Literal["YulVariableDeclaration"] = Field(alias="nodeType")
    # required
    variables: List["YulTypedName"]
    # optional
    value: OptionalYulExpressionUnion


class YulFunctionCall(YulNode):
    # override alias
    node_type: Literal["YulFunctionCall"] = Field(alias="nodeType")
    # required
    arguments: List[YulExpressionUnion]
    function_name: "YulIdentifier"
    # optional


class YulIdentifier(YulNode):
    # override alias
    node_type: Literal["YulIdentifier"] = Field(alias="nodeType")
    # required
    name: Name
    # optional


class YulLiteral(YulNode):
    # override alias
    node_type: Literal["YulLiteral"] = Field(alias="nodeType")
    # required
    kind: YulLiteralValueKind
    type: Type
    # at least one of these should be set
    value: Optional[Value]
    hex_value: Optional[HexValue]

    @root_validator
    def value_or_hex_value_set(cls, values):
        value, hex_value = values.get("value"), values.get("hex_value")
        assert (
            value is not None or hex_value is not None
        ), "YulLiteral: either 'value' or 'hex_value' must be set"
        return values


class YulTypedName(YulNode):
    # override alias
    node_type: Literal["YulTypedName"] = Field(alias="nodeType")
    # required
    name: Name
    type: Type
    # optional


class YulCase(YulNode):
    # override alias
    node_type: Literal["YulCase"] = Field(alias="nodeType")
    # required
    body: "YulBlock"
    value: Union[Literal["default"], YulLiteral]
    # optional


# region update_forward_refs
SolcSourceUnit.update_forward_refs()
SolcPragmaDirective.update_forward_refs()
SolcImportDirective.update_forward_refs()
SolcVariableDeclaration.update_forward_refs()
SolcEnumDefinition.update_forward_refs()
SolcFunctionDefinition.update_forward_refs()
SolcStructDefinition.update_forward_refs()
SolcErrorDefinition.update_forward_refs()
SolcUserDefinedValueTypeDefinition.update_forward_refs()
SolcContractDefinition.update_forward_refs()
SolcEventDefinition.update_forward_refs()
SolcModifierDefinition.update_forward_refs()
SolcUsingForDirective.update_forward_refs()
SolcArrayTypeName.update_forward_refs()
SolcElementaryTypeName.update_forward_refs()
SolcFunctionTypeName.update_forward_refs()
SolcMapping.update_forward_refs()
SolcUserDefinedTypeName.update_forward_refs()
SolcBlock.update_forward_refs()
SolcBreak.update_forward_refs()
SolcContinue.update_forward_refs()
SolcDoWhileStatement.update_forward_refs()
SolcEmitStatement.update_forward_refs()
SolcExpressionStatement.update_forward_refs()
SolcForStatement.update_forward_refs()
SolcIfStatement.update_forward_refs()
SolcInlineAssembly.update_forward_refs()
SolcPlaceholderStatement.update_forward_refs()
SolcReturn.update_forward_refs()
SolcRevertStatement.update_forward_refs()
SolcTryStatement.update_forward_refs()
SolcUncheckedBlock.update_forward_refs()
SolcVariableDeclarationStatement.update_forward_refs()
SolcWhileStatement.update_forward_refs()
SolcAssignment.update_forward_refs()
SolcBinaryOperation.update_forward_refs()
SolcConditional.update_forward_refs()
SolcElementaryTypeNameExpression.update_forward_refs()
SolcFunctionCall.update_forward_refs()
SolcFunctionCallOptions.update_forward_refs()
SolcIdentifier.update_forward_refs()
SolcIndexAccess.update_forward_refs()
SolcIndexRangeAccess.update_forward_refs()
SolcLiteral.update_forward_refs()
SolcMemberAccess.update_forward_refs()
SolcNewExpression.update_forward_refs()
SolcTupleExpression.update_forward_refs()
SolcUnaryOperation.update_forward_refs()
SolcOverrideSpecifier.update_forward_refs()
SolcIdentifierPath.update_forward_refs()
SolcParameterList.update_forward_refs()
SolcTryCatchClause.update_forward_refs()
SolcStructuredDocumentation.update_forward_refs()
SolcEnumValue.update_forward_refs()
SymbolAliasModel.update_forward_refs()
YulAssignment.update_forward_refs()
YulBlock.update_forward_refs()
YulBreak.update_forward_refs()
YulContinue.update_forward_refs()
YulExpressionStatement.update_forward_refs()
YulLeave.update_forward_refs()
YulForLoop.update_forward_refs()
YulFunctionDefinition.update_forward_refs()
YulIf.update_forward_refs()
YulSwitch.update_forward_refs()
YulVariableDeclaration.update_forward_refs()
YulFunctionCall.update_forward_refs()
YulIdentifier.update_forward_refs()
YulLiteral.update_forward_refs()
YulTypedName.update_forward_refs()
YulCase.update_forward_refs()
# endregion update_forward_refs
